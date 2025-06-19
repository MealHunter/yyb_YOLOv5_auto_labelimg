# 对数据集进行重命名
import os

# 设置图片和标签的文件夹路径
image_folder = 'C:/Users/admin/Desktop/2025-3-17/People Detection -General-.v4-v1-fast_model-aug3x.yolov5pytorch/images'  # 图片所在文件夹
label_folder = 'C:/Users/admin/Desktop/2025-3-17/People Detection -General-.v4-v1-fast_model-aug3x.yolov5pytorch/labels'  # 标签所在文件夹

# 支持的图片格式
image_exts = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')
label_ext = '.txt'

# 获取所有的图片和标签文件（不带扩展名）
image_files = sorted([f for f in os.listdir(image_folder) if f.lower().endswith(image_exts)])
label_files = sorted([f for f in os.listdir(label_folder) if f.lower().endswith(label_ext)])

# 统计不带扩展名的文件名
image_names = set(os.path.splitext(f)[0] for f in image_files)
label_names = set(os.path.splitext(f)[0] for f in label_files)

# 交集部分才是正确匹配的文件
common_names = sorted(image_names & label_names)

# 检查数据一致性
if not common_names:
    print("⚠️ 没有找到匹配的图片和标签文件，请检查数据！")
    exit()

# 进行重命名
for idx, name in enumerate(common_names, start=1):
    new_name = f"Person_Detect_{idx:06d}"  # 生成 6 位数编号，例如 000001, 000002 ...

    # 原文件路径
    old_image_path = os.path.join(image_folder, name + os.path.splitext(image_files[0])[1])  # 取图片的原格式
    old_label_path = os.path.join(label_folder, name + label_ext)

    # 新文件路径
    new_image_path = os.path.join(image_folder, new_name + os.path.splitext(image_files[0])[1])
    new_label_path = os.path.join(label_folder, new_name + label_ext)

    # 重命名文件
    os.rename(old_image_path, new_image_path)
    os.rename(old_label_path, new_label_path)

    print(f"✅ {name} -> {new_name}")

print("🎉 重命名完成！")
