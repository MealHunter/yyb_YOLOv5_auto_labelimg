# 删除没有标签的文件和图片
import os
import shutil

# 文件夹路径
label_folder = 'C:/Users/admin/Desktop/2025-3-17/labels'
image_folder = 'C:/Users/admin/Desktop/2025-3-17/images'

# 备份文件夹（存放将要删除的文件）
backup_labels = 'C:/Users/admin/Desktop/delect/labels'
backup_images = 'C:/Users/admin/Desktop/delect/images'

# 确保备份文件夹存在
os.makedirs(backup_labels, exist_ok=True)
os.makedirs(backup_images, exist_ok=True)

# 获取 label 文件夹中的所有 .txt 文件名（不带扩展名）
label_files = set()
for label_file in os.listdir(label_folder):
    label_path = os.path.join(label_folder, label_file)

    # 只处理 .txt 文件
    if label_file.endswith('.txt'):
        # 如果文件为空，移动到 backup_labels 文件夹
        if os.path.getsize(label_path) == 0:
            try:
                shutil.move(label_path, os.path.join(backup_labels, label_file))
                print(f"已移动空标签文件到备份文件夹：{label_file}")
            except Exception as e:
                print(f"移动空标签文件 {label_file} 失败: {e}")
        else:
            # 添加到标签集合
            label_files.add(os.path.splitext(label_file)[0])

# 遍历 image 文件夹中的所有图片文件
for image_file in os.listdir(image_folder):
    # 只处理常见的图片格式
    if image_file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp')):
        image_name = os.path.splitext(image_file)[0]

        # 如果图片没有对应的标签，则移动到 backup_images
        if image_name not in label_files:
            image_path = os.path.join(image_folder, image_file)
            try:
                shutil.move(image_path, os.path.join(backup_images, image_file))
                print(f"已移动图片到备份文件夹：{image_file}")
            except Exception as e:
                print(f"移动图片 {image_file} 失败: {e}")

print("处理完成！所有待删除文件已移动到备份文件夹。")


