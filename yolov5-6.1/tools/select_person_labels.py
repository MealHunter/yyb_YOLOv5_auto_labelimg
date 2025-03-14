# """遍历文件夹下的所有txt文件,同时筛选出所有人的标签"""
import os


def find_txt_files(directory):
    txt_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                txt_files.append(os.path.join(root, file))
    return txt_files


# 示例使用
directory_to_search = 'D:/YYB/project/yolov5-7.0/yolov5-7.0/datasets/COCO2017/COCO2017/COCO2017/label/val-original'  # 替换为你要遍历的目录路径
output_file_path = 'D:/YYB/project/yolov5-7.0/yolov5-7.0/datasets/COCO2017/COCO2017/COCO2017/label/val'  # 修改后文件存放路径
txt_files = find_txt_files(directory_to_search)
for txt_file in txt_files:
    print(txt_file)
    # 提取文件名（包括扩展名）
    file_name = os.path.basename(txt_file)

    # 构建新的文件路径
    new_file_path = os.path.join(output_file_path, file_name)

    # 打开文件以读取模式（'r'）打开，然后读取所有内容
    with open(txt_file, 'r', encoding='utf-8') as file:
        # file_contents = file.read()
        lines = file.readlines()

    filtered_lines = [line for line in lines if line.startswith('0')]

    # 将过滤后的内容写回到文件
    with open(new_file_path, 'w', encoding='utf-8') as file:
        file.writelines(filtered_lines)
print('处理完成')

# # 统计数据集当中有人的图片数量
# import os

# def count_files_with_first_number_14(folder_path):
#     count = 0  # 用于统计符合条件的.txt文件数量

#     # 遍历文件夹中的所有文件
#     for filename in os.listdir(folder_path):
#         # 只处理 .txt 文件
#         if filename.endswith(".txt"):
#             file_path = os.path.join(folder_path, filename)

#             try:
#                 with open(file_path, 'r') as file:
#                     # 遍历文件中的每一行
#                     for line in file:
#                         # 将行中的每个部分按空格拆分并检查第一个部分
#                         parts = line.split()
#                         if parts and parts[0] == "0":  # 如果行中有内容且第一个部分是 '14'
#                             count += 1
#                             break  # 如果找到了符合条件的行，则跳过当前文件的其他行
#             except Exception as e:
#                 print(f"无法读取文件 {filename}: {e}")

#     return count

# # 使用方法
# folder_path = "D:/YYB/project/yolov5-7.0/yolov5-7.0/datasets/COCO2017/COCO2017/label/train"  # 替换为你实际的文件夹路径
# result = count_files_with_first_number_14(folder_path)
# print(f"符合条件的.txt文件数量: {result}")


