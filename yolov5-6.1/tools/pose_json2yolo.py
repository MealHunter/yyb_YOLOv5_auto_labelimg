import os
import json
import math


def is_point_inside_bbox(point, bbox):
    """检查点是否在bounding box内"""
    x, y = point
    x_min, y_min = bbox[0]
    x_max, y_max = bbox[1]
    return x_min <= x <= x_max and y_min <= y <= y_max


# 输入文件
input_dir = "C:/Users/admin/Desktop/face/scrfd_label/scrfd_label/train/labelme_json"
output_dir = "C:/Users/admin/Desktop/face/scrfd_label/scrfd_label/train/labels"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 遍历 JSON 文件
for filename in os.listdir(input_dir):
    if filename.endswith(".json"):
        json_file_path = os.path.join(input_dir, filename)
        with open(json_file_path, "r") as json_file:
            json_data = json.load(json_file)

        image_width = json_data["imageWidth"]
        image_height = json_data["imageHeight"]
        shapes = json_data["shapes"]

        output_txt_path = os.path.join(output_dir, f"{filename.replace('.json', '.txt')}")

        with open(output_txt_path, "w") as txt_file:
            # 先收集所有关键点
            all_keypoints = [s for s in shapes if s["shape_type"] == "point"]

            # 处理所有bounding box
            for shape in shapes:
                if shape["shape_type"] == "rectangle" and shape["label"] == "face":
                    # 获取bounding box坐标
                    bbox = shape["points"]
                    x_min, y_min = bbox[0]
                    x_max, y_max = bbox[1]

                    # 计算中心点和宽高并归一化
                    norm_x_center = (x_min + x_max) / 2 / image_width
                    norm_y_center = (y_min + y_max) / 2 / image_height
                    norm_width = (x_max - x_min) / image_width
                    norm_height = (y_max - y_min) / image_height

                    # 写入bounding box信息
                    txt_file.write(f"0 {norm_x_center:.6f} {norm_y_center:.6f} {norm_width:.6f} {norm_height:.6f}")

                    # 收集属于当前bounding box的关键点
                    bbox_keypoints = {}
                    for kp in all_keypoints:
                        if kp["label"].startswith("keypoint_"):
                            point = kp["points"][0]
                            if is_point_inside_bbox(point, bbox):
                                try:
                                    kp_index = int(kp["label"].split("_")[1])
                                    bbox_keypoints[kp_index] = point
                                except (IndexError, ValueError):
                                    continue

                    # 按顺序写入关键点(0-4)
                    for i in range(5):  # 假设有5个关键点
                        if i in bbox_keypoints:
                            kp_x, kp_y = bbox_keypoints[i]
                            norm_kp_x = kp_x / image_width
                            norm_kp_y = kp_y / image_height
                            txt_file.write(f" {norm_kp_x:.6f} {norm_kp_y:.6f}")
                        else:
                            # 如果关键点缺失，写入0 0
                            txt_file.write(" 0 0")

                    txt_file.write("\n")

print(f"转换完成！TXT 文件保存在 {output_dir}/ 目录下")