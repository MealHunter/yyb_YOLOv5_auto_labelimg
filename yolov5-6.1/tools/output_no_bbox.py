import cv2
import os

def extract_frames_without_green_boxes(video_path, output_dir, green_color=(0, 255, 0), threshold=100):
    """
    提取视频中没有绿色框的帧。

    参数:
        video_path (str): 视频文件路径。
        output_dir (str): 输出图片的目录。
        green_color (tuple): 绿色框的颜色（BGR格式）。
        threshold (int): 绿色像素点的数量阈值。
    """
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

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

        # 检查是否存在绿色框
        green_mask = cv2.inRange(frame, green_color, green_color)
        green_pixel_count = cv2.countNonZero(green_mask)

        # 如果没有绿色框，保存该帧
        if green_pixel_count < threshold:
            output_path = os.path.join(output_dir, f"frame_{frame_count:04d}.png")
            cv2.imwrite(output_path, frame)
            saved_count += 1
            print(f"保存帧: {output_path}")

    # 释放视频对象
    cap.release()
    print(f"视频处理完成。总帧数: {frame_count}, 保存帧数: {saved_count}")

if __name__ == "__main__":
    # 设置视频路径和输出目录
    video_path = "C:/Users/admin/Desktop/效果录像/output.mp4"  # 替换为你的视频路径
    output_dir = "C:/Users/admin/Desktop/效果录像/123"  # 替换为你的输出目录

    # 提取没有绿色框的帧
    extract_frames_without_green_boxes(video_path, output_dir)
