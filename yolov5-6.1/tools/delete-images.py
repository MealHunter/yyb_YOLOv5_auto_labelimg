# 删除没有标签的文件和图片
import os

# 文件夹路径
label_folder = 'C:/Users/admin/Desktop/video2/labels-txt'
image_folder = 'C:/Users/admin/Desktop/video2/images'

# 获取 label 文件夹中的所有 .txt 文件名（不带扩展名）
label_files = set(os.path.splitext(f)[0] for f in os.listdir(label_folder) if f.endswith('.txt'))

# 遍历 label 文件夹中的所有 .txt 文件，删除空的标签文件
for label_file in os.listdir(label_folder):
    label_path = os.path.join(label_folder, label_file)
    
    # 如果是 .txt 文件且为空，删除该标签文件
    if label_file.endswith('.txt') and os.path.getsize(label_path) == 0:
        os.remove(label_path)
        print(f"已删除空标签文件：{label_file}")

# 获取更新后的 label 文件名（删除空标签文件后的）
label_files = set(os.path.splitext(f)[0] for f in os.listdir(label_folder) if f.endswith('.txt'))

# 遍历 image 文件夹中的所有图片文件
for image_file in os.listdir(image_folder):
    # 获取文件名（不带扩展名）
    image_name = os.path.splitext(image_file)[0]

    # 如果 image 文件夹中的文件名在 label 文件夹中不存在，则删除该图片
    if image_name not in label_files:
        image_path = os.path.join(image_folder, image_file)
        os.remove(image_path)
        print(f"已删除图片：{image_file}")

print("处理完成！")
