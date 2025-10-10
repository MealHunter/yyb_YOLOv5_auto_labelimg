import cv2
import numpy as np
import os
import re

def remove_green_boxes(frame):
    """
    识别并去除图像中的绿色框，并用周围像素填充。
    """
    # 转换到 HSV 颜色空间
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 绿色的 HSV 范围
    lower_green = np.array([35, 100, 100])  # 绿色下界
    upper_green = np.array([85, 255, 255])  # 绿色上界

    # 创建绿色掩码
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # 使用 inpaint 修复去除绿色框后的区域
    frame_without_green = cv2.inpaint(frame, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

    return frame_without_green

def get_start_index(output_dir):
    """
    获取已存在的最大帧编号，返回下一个编号
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        return 145  # 如果目录不存在，从 145 开始

    max_index = 986  # 设定最小起始编号
    pattern = re.compile(r"chair_(\d{5})\.jpg")

    for filename in os.listdir(output_dir):
        match = pattern.match(filename)
        if match:
            max_index = max(max_index, int(match.group(1)))

    return max_index + 1

def extract_frames_and_remove_green_boxes(video_path, output_dir):
    """
    提取视频帧，去除绿色框后保存。

    参数:
        video_path (str): 视频文件路径。
        output_dir (str): 输出图片的目录。
    """
    # 确定帧起始编号
    start_index = get_start_index(output_dir)

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"无法打开视频文件: {video_path}")
        return

    frame_count = 0
    saved_count = 0

    while True:
        # 读取一帧
        ret, frame = cap.read()
        if not ret:
            break  # 视频结束

        frame_count += 1

        # 去除绿色框
        frame_cleaned = remove_green_boxes(frame)

        # 保存处理后的帧
        output_path = os.path.join(output_dir, f"chair_{start_index:05d}.jpg")
        cv2.imwrite(output_path, frame_cleaned)
        start_index += 1  # 继续累加
        saved_count += 1
        print(f"保存帧: {output_path}")

    # 释放视频对象
    cap.release()
    print(f"视频处理完成。总帧数: {frame_count}, 保存帧数: {saved_count}")

if __name__ == "__main__":
    # 设置视频路径和输出目录
    video_path = "C:/Users/admin/Desktop/2025-3-17/7-3.mp4"  # 替换为你的视频路径
    output_dir = "C:/Users/admin/Desktop/2025-3-17/6_27/6_27/images"  # 替换为你的输出目录

    # 处理视频，去除绿色框并保存帧
    extract_frames_and_remove_green_boxes(video_path, output_dir)
