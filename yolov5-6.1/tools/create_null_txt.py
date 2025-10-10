# 创建空白的txt文件
import os

# 设置文件夹路径
folder_path = "C:/Users/admin/Desktop/2025-3-17/6_27/6_27/images"  # 替换为你的文件夹路径
txt_path = "C:/Users/admin/Desktop/2025-3-17/6_27/6_27/labels"

# 支持的图片扩展名
image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"}

# 遍历文件夹中的文件
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    # 检查是否是图片文件
    if os.path.isfile(file_path) and any(filename.lower().endswith(ext) for ext in image_extensions):
        # 创建同名的 .txt 文件
        txt_filename = os.path.splitext(filename)[0] + ".txt"
        txt_file_path = os.path.join(txt_path, txt_filename)

        # 如果 .txt 文件不存在，则创建
        if not os.path.exists(txt_file_path):
            with open(txt_file_path, "w") as txt_file:
                txt_file.write("")  # 创建一个空文件
            print(f"Created: {txt_filename}")
        else:
            print(f"Already exists: {txt_filename}")

print("文本文件创建成功")
