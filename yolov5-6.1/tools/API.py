from fastapi import FastAPI, HTTPException, Query
import cv2
import insightface
import requests
import numpy as np
import uvicorn
import pymysql
import json
from insightface.app import FaceAnalysis 


app = FastAPI() 
# Initialize face analysis model
face_app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])  # Use 'CUDAExecutionProvider' for GPU
face_app.prepare(ctx_id=-1)  # ctx_id=-1 for CPU, 0 for GPU


# =========================
# 数据库连接配置
# =========================
def get_db_connection():
    return pymysql.connect(
        host="192.168.1.114",
        user="bi-read",
        password="5!tVwfZzqwSU^uWX",
        database="pms",
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor
    )

def get_face_embedding_from_url(image_url: str): 
    """从网络图片提取人脸 embedding"""
    try:
        # 下载图片
        resp = requests.get(image_url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"下载图片失败: {e}")

    # 转为 OpenCV 格式
    img_array = np.frombuffer(resp.content, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(status_code=400, detail="无法解析为有效图片")

    # 提取人脸
    faces = face_app.get(img) 
    if len(faces) < 1:
        raise HTTPException(status_code=404, detail="未检测到人脸") 
    if len(faces) > 1:
        print("⚠️ 检测到多张人脸，仅使用第一张")

    # 获取人脸 embedding 
    emb = faces[0].embedding
    return emb.tolist()  # 转为 Python list 方便 JSON 输出

def compare_faces(emb1, emb2, threshold=0.65): # Adjust this threshold according to your usecase.
    """Compare two embeddings using cosine similarity"""
    similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
    return similarity, similarity > threshold
   
@app.post("/getFaceFeature")
async def get_face_feature(image_url: str = Query(..., description="图片URL")):
    emb = get_face_embedding_from_url(image_url)
    return {
        "msg": "ok",
        "image_url": image_url,
        "embedding": emb
    }

@app.post("/composeFaceFeature") 
async def compose_face_feature(image: str = Query(..., description="图片1 URL"),
                               device_id: str = Query("", description="设备ID"),
                               team_id: int = Query(0, description="团队ID"),
                               source_type: int = Query(0, description="数据来源")):
    emb = get_face_embedding_from_url(image)
    
    # 获取数据库中的人脸特征
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """SELECT df.device_id,uf.team_id,df.face_id,uf.face_name,uf.face_eigenvalue
              FROM t_pms_device_face_info AS df
              LEFT JOIN t_pms_user_face_info AS uf ON df.face_id = uf.id
              WHERE df.device_id = %s
              AND uf.team_id = %s
              AND df.source_type = %s
              AND df.face_type = 1
              AND df.import_status = 1
              AND df.del_flag = 0"""
    cursor.execute(sql, (device_id, team_id, source_type))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="数据库中无可用人脸特征")
    
    results = []
    for row in rows:
        try:
            emb_lib = np.array(json.loads(row["face_eigenvalue"]), dtype=np.float32)
            sim, same = compare_faces(emb, emb_lib)
            results.append({
                "face_id": row["face_id"],
                "similarity": float(sim),
                "is_same_person": same
            })
        except Exception as e:
            print(f"⚠️ 特征解析错误 {row['face_id']}: {e}")

    # 返回最高相似度结果
    best_match = max(results, key=lambda x: x["similarity"]) if results else None

    return {
        "msg": "ok",
        "input_image": image,
        "best_match": best_match,
        "all_results": results[:5]  # 可选：返回前5个最相似
    }
 
 
if __name__ == "__main__":

    print("运行成功")
    uvicorn.run(app, host = "0.0.0.0", port = 9001)
 
