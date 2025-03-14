import xml.etree.ElementTree as ET
import os
import shutil
import random
 
 
def convert(size, box):
    x_center = (box[0] + box[1]) / 2.0
    y_center = (box[2] + box[3]) / 2.0
    x = x_center / size[0]
    y = y_center / size[1]
    w = (box[1] - box[0]) / size[0]
    h = (box[3] - box[2]) / size[1]
    return (x, y, w, h)
 
 
def convert_annotation(xml_files_path, save_txt_files_path, classes):
    xml_files = os.listdir(xml_files_path)
    print(xml_files)
    for xml_name in xml_files:
        print(xml_name)
        xml_file = os.path.join(xml_files_path, xml_name)
        out_txt_path = os.path.join(save_txt_files_path, xml_name.split('.')[0] + '.txt')
        out_txt_f = open(out_txt_path, 'w')
        tree = ET.parse(xml_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
 
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            # b=(xmin, xmax, ymin, ymax)
            print(w, h, b)
            bb = convert((w, h), b)
            out_txt_f.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


def delect_images(image_folder, label_folder):
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


def split_images(image_dir, label_dir,train_image_dir,val_image_dir,train_label_dir,val_label_dir):
    # 创建训练集和验证集文件夹
    os.makedirs(train_image_dir, exist_ok=True)
    os.makedirs(val_image_dir, exist_ok=True)
    os.makedirs(train_label_dir, exist_ok=True)
    os.makedirs(val_label_dir, exist_ok=True)

    # 获取所有图片文件
    image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png'))]

    # 打乱图片文件列表
    random.shuffle(image_files)

    # 按照8:2的比例划分训练集和验证集
    split_index = int(0.8 * len(image_files))

    train_images = image_files[:split_index]
    val_images = image_files[split_index:]

    # 将图片和标签移动到对应的文件夹
    for image_file in train_images:
        label_file = image_file.replace('.jpg', '.txt').replace('.png', '.txt')

        # 移动图片
        shutil.move(os.path.join(image_dir, image_file), os.path.join(train_image_dir, image_file))

        # 移动标签
        if os.path.exists(os.path.join(label_dir, label_file)):
            shutil.move(os.path.join(label_dir, label_file), os.path.join(train_label_dir, label_file))

    for image_file in val_images:
        label_file = image_file.replace('.jpg', '.txt').replace('.png', '.txt')

        # 移动图片
        shutil.move(os.path.join(image_dir, image_file), os.path.join(val_image_dir, image_file))

        # 移动标签
        if os.path.exists(os.path.join(label_dir, label_file)):
            shutil.move(os.path.join(label_dir, label_file), os.path.join(val_label_dir, label_file))

    print("数据划分完成！")
 
 
if __name__ == "__main__":
# 将.xml文件转换为.txt文件
    # 需要转换的类别，需要一一对应
    classes1 = ['person']
    # 2、voc格式的xml标签文件路径
    xml_files1 = 'C:/Users/admin/Desktop/vi/labels'
    # 3、转化为yolo格式的txt标签文件存储路径
    save_txt_files1 = 'C:/Users/admin/Desktop/vi/labels-txt'
    convert_annotation(xml_files1, save_txt_files1, classes1)

# # 根据.txt文件名删除没有目标的.txt文件和对应的图片
#     image_folder = 'D:/YYB/project/yolov5-7.0/yolov5-7.0/datasets/myself/video/YouTube/images'
#
#     delect_images(image_folder, save_txt_files1)  # (images,labels)
#
# # 按照8：2的比例划分数据集
#     train_image_dir = 'D:/YYB/project/yolov5-7.0/yolov5-7.0/datasets/myself/video/bilibili/person/images/train'  # 训练集图片存放路径
#     val_image_dir = 'D:/YYB/project/yolov5-7.0/yolov5-7.0/datasets/myself/video/bilibili/person/images/val'  # 验证集图片存放路径
#     train_label_dir = 'D:/YYB/project/yolov5-7.0/yolov5-7.0/datasets/myself/video/bilibili/person/labels/train'  # 训练集标签存放路径
#     val_label_dir = 'D:/YYB/project/yolov5-7.0/yolov5-7.0/datasets/myself/video/bilibili/person/labels/val'  # 验证集标签存放路径
#     split_images(image_folder, save_txt_files1, train_image_dir, train_label_dir, val_image_dir, val_label_dir)



