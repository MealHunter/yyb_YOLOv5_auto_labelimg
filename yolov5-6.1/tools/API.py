from fastapi import FastAPI


app = FastAPI() 


@app.post("/getFaceFeature")
async def get_face_feature(image: str):
    
    return {"msg": "ok"}



if __name__ == "__main__":
    import uvicorn
    print("运行成功")
    uvicorn.run(app, host = "0.0.0.0", port = 9001)
