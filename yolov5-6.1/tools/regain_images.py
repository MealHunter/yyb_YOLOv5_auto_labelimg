import os

# 设置文件夹路径和 file.txt 路径
folder_path = "C:/Users/admin/Desktop/video2/images"  # 替换为你的文件夹路径
txt_file_path = os.path.join(folder_path, "123.txt")  # file.txt 的路径

# 读取 file.txt 中的文件名
with open(txt_file_path, "r") as file:
    files_to_keep = set(line.strip() for line in file)  # 使用集合提高查找效率

# 遍历文件夹中的文件
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    # 如果是文件且不在 file.txt 中，则删除
    if os.path.isfile(file_path) and filename not in files_to_keep:
        os.remove(file_path)
        print(f"Deleted: {filename}")
    else:
        print(f"Kept: {filename}")

print("图片已经恢复")
