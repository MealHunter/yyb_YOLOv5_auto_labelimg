# import os
#
# # 路径设置
# nv12_dir = "C:/Users/admin/Desktop/123/nv12"  # 原始 .nv12 文件夹C:/Users/admin/Desktop/123/nv12/nv12
# txt_dir = "C:/Users/admin/Desktop/456/images"    # 待清理 .txt 文件夹
#
# # 获取 .nv12 文件的基名（不含扩展名）
# nv12_names = {os.path.splitext(f)[0] for f in os.listdir(nv12_dir) if f.endswith(".nv12")}
#
# # 删除不在 nv12_names 中的 .txt 文件
# for f in os.listdir(txt_dir):
#     if f.endswith(".png"):
#         base = os.path.splitext(f)[0]
#         if base not in nv12_names:
#             file_path = os.path.join(txt_dir, f)
#             print(f"Deleting: {file_path}")
#             os.remove(file_path)

# import os
#
# # 路径设置
# nv12_dir = "C:/Users/admin/Desktop/person/labels/train"  # A 文件夹，含 .nv12 文件
# png_dir = "C:/Users/admin/Desktop/person/images/train"  # B 文件夹，含 .png 文件
#
# # 获取 A 文件夹中所有 .nv12 文件的基本名
# nv12_names = {os.path.splitext(f)[0] for f in os.listdir(nv12_dir) if f.endswith(".txt")}
#
#
# # 获取 B 文件夹中所有图像文件的基本名
# image_names = {os.path.splitext(f)[0] for f in os.listdir(png_dir) if f.endswith((".png", ".jpg"))}
#
#
# # 找出 A 有但 B 没有的文件名
# missing_pngs = nv12_names - image_names
#
# # 输出缺失信息
# if missing_pngs:
#     print("B 文件夹中缺少以下 .png 文件：")
#     for name in sorted(missing_pngs):
#         print(name + ".png")
# else:
#     print("B 文件夹中没有缺失任何对应的 .png 文件。")


import os

# 替换为你的实际路径
folder_a = 'C:/Users/admin/Desktop/person/labels/train'
folder_b = 'C:/Users/admin/Desktop/junz/456/labels_or/labels_or/labels_or'

# 获取 B 文件夹中所有 txt 文件名（不含路径）
b_txt_filenames = {f for f in os.listdir(folder_b) if f.endswith('.txt')}

# 遍历 A 文件夹中的所有 txt 文件
for file_name in os.listdir(folder_a):
    if file_name.endswith('.txt') and file_name in b_txt_filenames:
        file_path = os.path.join(folder_a, file_name)
        try:
            os.remove(file_path)
            print(f"已删除: {file_path}")
        except Exception as e:
            print(f"删除失败 {file_path}: {e}")



