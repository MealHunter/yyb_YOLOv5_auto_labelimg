import os
import shutil

# 设置原始的 train 文件夹路径
train_dir = 'C:/Users/admin/Desktop/face/WIDER_train/WIDER_train/images'  # 根据你的实际路径调整

# 遍历 train 文件夹中的所有子文件夹
for root, dirs, files in os.walk(train_dir):
    for file in files:
        # 只处理图片文件，可以根据需要修改文件类型
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            # 构造源文件路径
            src = os.path.join(root, file)

            # 确保文件不在 train 目录本身中
            if root != train_dir:
                # 构造目标文件路径，将文件移动到 train 文件夹
                dst = os.path.join(train_dir, file)

                # 如果目标路径已存在，则重命名文件（防止覆盖）
                if os.path.exists(dst):
                    base, ext = os.path.splitext(file)
                    counter = 1
                    while os.path.exists(dst):
                        dst = os.path.join(train_dir, f"{base}_{counter}{ext}")
                        counter += 1

                # 移动文件
                shutil.move(src, dst)
                print(f"Moved: {src} -> {dst}")
