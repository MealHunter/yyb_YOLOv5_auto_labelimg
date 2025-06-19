import os
import cv2

# 配置路径
image_dir = "C:/Users/admin/Desktop/junz/new/images/images"  # 图像目录
label_dir = "C:/Users/admin/Desktop/junz/456/new/6-result"  # 标签目录
output_dir = "C:/Users/admin/Desktop/junz/456/new/6-output"  # 绘制后图像保存目录

os.makedirs(output_dir, exist_ok=True)

# 类别映射（可按需要修改）
class_names = ['person', 'car', 'dog']

# 遍历图像文件
for img_name in os.listdir(image_dir):
    if not img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue

    img_path = os.path.join(image_dir, img_name)
    label_path = os.path.join(label_dir, os.path.splitext(img_name)[0] + '.txt')

    # 读取图片
    img = cv2.imread(img_path)
    h, w = img.shape[:2]

    # 读取标签
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            for line in f.readlines():
                parts = line.strip().split()
                if len(parts) != 5:
                    continue

                class_id, x_center, y_center, width, height = map(float, parts)
                class_id = int(class_id)

                # 将归一化坐标还原
                x_center *= w
                y_center *= h
                width *= w
                height *= h

                # 计算左上角坐标
                x1 = int(x_center - width / 2)
                y1 = int(y_center - height / 2)
                x2 = int(x_center + width / 2)
                y2 = int(y_center + height / 2)

                # 绘制矩形框
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # 绘制类别文字
                label = class_names[class_id] if class_id < len(class_names) else str(class_id)
                cv2.putText(img, label, (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # 保存绘制后的图像
    out_path = os.path.join(output_dir, img_name)
    cv2.imwrite(out_path, img)

print("绘图完成，保存于：", output_dir)
