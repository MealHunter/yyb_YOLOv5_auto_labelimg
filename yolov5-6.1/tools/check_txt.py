import os

def check_first_number_is_zero(folder_path):
    """
    检查文件夹下所有 .txt 文件中每一行的第一个数字是否为 0。

    参数:
        folder_path (str): 包含 .txt 文件的文件夹路径。
    """
    # 存储包含非 0 开头的行的文件名
    invalid_files = []

    # 遍历文件夹下的所有文件
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r") as file:
                for line_num, line in enumerate(file, start=1):
                    # 去掉行首尾的空白字符
                    line = line.strip()
                    if line:  # 跳过空行
                        # 分割行内容
                        parts = line.split()
                        if parts:  # 确保行不为空
                            try:
                                first_number = float(parts[0])  # 尝试将第一个值转换为数字
                                if first_number != 0:
                                    invalid_files.append(file_name)
                                    break  # 只要有一行不符合条件，就记录文件名并跳出
                            except ValueError:
                                print(f"警告: 文件 {file_name} 的第 {line_num} 行格式错误: {line}")

    # 输出结果
    if invalid_files:
        print("以下文件的某些行第一个数字不是 0:")
        for file_name in invalid_files:
            print(file_name)
    else:
        print("所有文件的每一行第一个数字均为 0。")

if __name__ == "__main__":
    # 设置文件夹路径
    folder_path = "C:/Users/admin/Desktop/person/labels/val"  # 替换为你的文件夹路径

    # 检查文件
    check_first_number_is_zero(folder_path)
