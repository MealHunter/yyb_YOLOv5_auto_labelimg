import cv2
import os


# 计算拉普拉斯变换的方差，用于评估图像的清晰度
def is_blurry(image, threshold=100.0):
    laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()
    return laplacian_var < threshold


# 提取视频帧并筛选
def extract_frames(video_path, output_folder, frame_interval=23, blur_threshold=150.0): #370
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    frame_index = 0
    frame_number = 0  # 用于计数帧数

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_number += 1

        # 每隔 `frame_interval` 帧提取一张图片
        if frame_number % frame_interval == 0:
            # 转换为灰度图
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 判断当前帧是否模糊
            if is_blurry(gray_frame, blur_threshold):
                print(f"跳过模糊帧: youtobe_{frame_index:05d}")
                continue

            # 保存清晰帧
            frame_filename = os.path.join(output_folder, f"company_{frame_index:05d}.jpg")
            cv2.imwrite(frame_filename, frame)
            print(f"保存帧: {frame_filename}")
            frame_index += 1

    cap.release()
    print(f"总共保存了 {frame_index} 张清晰帧")


# 使用示例
video_path = 'C:/Users/admin/Desktop/video/output.mp4'
output_folder = 'C:/Users/admin/Desktop/video2/images'  # 指定保存的文件夹
extract_frames(video_path, output_folder)

# import cv2
# import numpy as np
# import os

# # 计算均方误差 (MSE)
# def mse(imageA, imageB):
#     return np.sum((imageA - imageB) ** 2) / float(imageA.shape[0] * imageA.shape[1])

# # 计算拉普拉斯变换的方差，用于评估图像的清晰度
# def is_blurry(image, threshold=100.0):
#     laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()
#     return laplacian_var < threshold

# # 提取视频帧并筛选
# def extract_frames(video_path, output_folder, diff_threshold=50.0, blur_threshold=350.0):
#     # 确保输出文件夹存在
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

#     # 打开视频文件
#     cap = cv2.VideoCapture(video_path)
#     ret, prev_frame = cap.read()
#     prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

#     frame_count = 0
#     frame_index = 0

#     while ret:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         frame_count += 1

#         # 转换当前帧为灰度图
#         gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         # 计算当前帧和前一帧的MSE差异
#         diff = mse(prev_frame_gray, gray_frame)

#         # 判断当前帧是否模糊
#         if is_blurry(gray_frame, blur_threshold):
#             print(f"跳过模糊帧: frame_{frame_index:04d}")
#             prev_frame_gray = gray_frame
#             continue

#         # 如果差异大于阈值，则保存当前帧
#         if diff > diff_threshold:
#             frame_filename = os.path.join(output_folder, f"frame_{frame_index:04d}.jpg")
#             cv2.imwrite(frame_filename, frame)
#             print(f"保存帧: {frame_filename}")
#             frame_index += 1

#         # 更新上一帧
#         prev_frame_gray = gray_frame

#     cap.release()
#     print(f"总共保存了 {frame_index} 张关键帧")

# # 使用示例
# video_path = 'D:/YYB/project/yolov5-7.0/yolov5-7.0/datasets/myself/video/12-27/ok_video.mp4'
# output_folder = 'D:/YYB/project/yolov5-7.0/yolov5-7.0/datasets/myself/video/12-27/images'  # 指定保存的文件夹
# extract_frames(video_path, output_folder)


