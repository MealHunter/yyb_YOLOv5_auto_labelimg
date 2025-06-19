## wife转YOLO（一步完成）
# import os
#
# # 读取 labels.txt
# input_file = "C:/Users/admin/Desktop/face/scrfd_label/scrfd_label/train/labelv2.txt"  # 修改为你的 labels 文件路径
# output_dir = "C:/Users/admin/Desktop/face/scrfd_label/scrfd_label/train/labels_yolo"  # 输出目录
#
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)
#
# with open(input_file, "r") as f:
#     lines = f.readlines()
#
# current_image = None
# image_width, image_height = 1, 1  # 初始化
# annotations = []
#
# for line in lines:
#     line = line.strip()
#     if not line:
#         continue
#
#     # 处理图片信息
#     if line.startswith("#"):
#         if current_image and annotations:
#             output_path = os.path.join(output_dir, f"{current_image}.txt")
#             with open(output_path, "w") as out_f:
#                 out_f.writelines(annotations)
#
#         # 解析 "# 图片路径 width height"
#         parts = line.split()
#         current_image = parts[1].split("/")[-1].replace(".jpg", "")
#         image_width, image_height = int(parts[2]), int(parts[3])
#         annotations = []
#         continue
#
#     # 解析目标框和关键点
#     values = list(map(float, line.split()))
#     x_min, y_min, x_max, y_max = values[:4]
#     keypoints = values[4:]
#
#     # 计算 bbox
#     x_center = (x_min + x_max) / 2 / image_width
#     y_center = (y_min + y_max) / 2 / image_height
#     w = (x_max - x_min) / image_width
#     h = (y_max - y_min) / image_height
#
#     # 处理关键点 (x, y, v)
#     yolo_keypoints = []
#     for i in range(0, len(keypoints), 3):
#         x, y = keypoints[i], keypoints[i + 1]  #, keypoints[i + 2]
#         if x == -1 or y == -1:
#             yolo_keypoints.extend(["0", "0", "0"])  # 不可见点
#         else:
#             yolo_keypoints.append(f"{x / image_width:.6f}")
#             yolo_keypoints.append(f"{y / image_height:.6f}")
#             #yolo_keypoints.append(str(int(v)))  # 可见性为整数
#
#     # 生成 YOLOv8-Pose 格式的行
#     annotation_line = f"0 {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f} " + " ".join(yolo_keypoints) + "\n"
#     annotations.append(annotation_line)
#
# # 处理最后一张图片的标签
# if current_image and annotations:
#     output_path = os.path.join(output_dir, f"{current_image}.txt")
#     with open(output_path, "w") as out_f:
#         out_f.writelines(annotations)
#
# print(f"转换完成！标注文件保存在 {output_dir}/ 目录下")


# wife转json（可以使用labelme查看）
import os
import json

# 输入文件
input_file = "C:/Users/admin/Desktop/face/scrfd_label/scrfd_label/train/labelv2.txt"  # 你的 labels 文件
output_dir = "C:/Users/admin/Desktop/face/scrfd_label/scrfd_label/train/labelme_json"  # 输出 JSON 目录

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(input_file, "r") as f:
    lines = f.readlines()

current_image = None
image_width, image_height = 1, 1
shapes = []

for line in lines:
    line = line.strip()
    if not line:
        continue

    # 处理图片信息
    if line.startswith("#"):
        if current_image and shapes:
            output_path = os.path.join(output_dir, f"{current_image}.json")
            json_data = {
                "version": "4.5.9",
                "flags": {},
                "shapes": shapes,
                "imagePath": f"{current_image}.jpg",
                "imageData": None,
                "imageHeight": image_height,
                "imageWidth": image_width,
            }
            with open(output_path, "w") as out_f:
                json.dump(json_data, out_f, indent=4)

        # 解析 "# 图片路径 width height"
        parts = line.split()
        current_image = parts[1].split("/")[-1].replace(".jpg", "")
        image_width, image_height = int(parts[2]), int(parts[3])
        shapes = []
        continue

    # 解析目标框和关键点
    values = list(map(float, line.split()))
    x_min, y_min, x_max, y_max = values[:4]
    keypoints = values[4:]

    # 添加 bounding box
    shapes.append({
        "label": "face",
        "points": [[x_min, y_min], [x_max, y_max]],
        "group_id": None,
        "shape_type": "rectangle",
        "flags": {}
    })

    # 添加关键点
    for i in range(0, len(keypoints), 3):
        x, y, v = keypoints[i], keypoints[i + 1], keypoints[i + 2]
        if x == -1 or y == -1:
            continue  # 跳过不可见点
        shapes.append({
            "label": f"keypoint_{i//3}",
            "points": [[x, y]],
            "group_id": None,
            "shape_type": "point",
            "flags": {}
        })

# 处理最后一张图片
if current_image and shapes:
    output_path = os.path.join(output_dir, f"{current_image}.json")
    json_data = {
        "version": "4.5.9",
        "flags": {},
        "shapes": shapes,
        "imagePath": f"{current_image}.jpg",
        "imageData": None,
        "imageHeight": image_height,
        "imageWidth": image_width,
    }
    with open(output_path, "w") as out_f:
        json.dump(json_data, out_f, indent=4)

print(f"转换完成！JSON 文件保存在 {output_dir}/ 目录下")

