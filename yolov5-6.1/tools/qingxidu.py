import cv2
import numpy as np
import matplotlib.pyplot as plt


from scipy.ndimage import gaussian_filter1d  # 若无 scipy，可改用 numpy.convolve


def mot_block_minmax(block):
    """原始方法，用 min/max —— 不稳健"""
    I_max = np.max(block)
    I_min = np.min(block)
    return (I_max - I_min) / (I_max + I_min) if (I_max + I_min) != 0 else 0

def mot_block_percentile(block, low_p=5, high_p=95):
    """用百分位(默认5%/95%)来代替 min/max,抗离群点"""
    vals = block.ravel()
    I_min = np.percentile(vals, low_p)
    I_max = np.percentile(vals, high_p)
    return (I_max - I_min) / (I_max + I_min) if (I_max + I_min) != 0 else 0

def mot_columnwise_average(block):
    """按列先算对比，再对列平均（减少块内像素极端点影响）"""
    # block shape: H x W_block
    col_max = block.max(axis=0).astype(float)
    col_min = block.min(axis=0).astype(float)
    denom = (col_max + col_min)
    # 防止除0
    valid = denom != 0
    col_contrast = np.zeros_like(col_max)
    col_contrast[valid] = (col_max[valid] - col_min[valid]) / denom[valid]
    return np.mean(col_contrast)

def smooth_list(lst, sigma=2):
    """高斯平滑(需要 scipy)没有则用简单滑动平均"""
    try:
        return gaussian_filter1d(np.array(lst), sigma=sigma)
    except Exception:
        # 简单移动平均窗口
        w = int(max(1, sigma*2+1))
        kernel = np.ones(w)/w
        return np.convolve(lst, kernel, mode='same')

# === 中间参数设置 ===
section_width = 10
start = 5
end = 20
x1 = 1976     #1445
y1 = 1016     #851
x2 = 2611     #1877
y2 = 1100     #903

# section_width = 6
# start = 8
# end = 13
# === 左上参数设置 ===
# x1 = 547     #1445
# y1 = 435     #851
# x2 = 815     #1877
# y2 = 479     #903

# === 左下参数设置 ===
# x1 = 535     #1445
# y1 = 1580     #851
# x2 = 801     #1877
# y2 = 1632     #903

# === 右上参数设置 ===
# x1 = 2961     #1445
# y1 = 453     #851
# x2 = 3233     #1877
# y2 = 501     #903

# === 右下参数设置 ===
# x1 = 2946     #1445
# y1 = 1620     #851
# x2 = 3220     #1877
# y2 = 1664     #903



# === Step 1: 读取图像 ===
img = cv2.imread('./tools/20250928.png', cv2.IMREAD_GRAYSCALE)
                                #                y1    y2   x1   x2
roi = img[y1:y2, x1:x2]         # 选定楔形区域    1016:1100, 1976:2611
height, width = roi.shape
print(f"ROI Size: {height}x{width}")

# # 显示 ROI 图像
# plt.imshow(roi, cmap='gray')
# plt.title("ROI Image")
# plt.axis('off')  # 隐藏坐标轴
# plt.show()

# === Step 2: 频率段划分（等宽分块）===
num_sections = width // section_width
print(f"Section Width: {section_width}")
# mot_values = []
mot_values_raw = []
mot_values_pct = []
mot_values_col = []
frequencies = []

cutoff_idx = None  # 初始化临界下标
MTF_THRESHOLD = 0.95  # ✅ 修改截止阈值为 0.03

for i in range(num_sections):
    x_start = i * section_width
    x_end = x_start + section_width
    block = roi[:, x_start:x_end]

    # I_max = np.max(block)
    # I_min = np.min(block)
    # mot = (I_max - I_min) / (I_max + I_min) if (I_max + I_min) != 0 else 0
    # mot = mot_block_percentile(block)

    mot_raw = mot_block_minmax(block)
    mot_pct = mot_block_percentile(block, low_p=5, high_p=95)
    mot_col = mot_columnwise_average(block)

    mot_values_raw.append(mot_raw)
    mot_values_pct.append(mot_pct)
    mot_values_col.append(mot_col)

    # mot_values.append(mot)
    tv_line = np.interp(i + 0.5, [0, num_sections], [start, end])
    frequencies.append(tv_line) 

    # if cutoff_idx is None and mot < MTF_THRESHOLD:
    #     cutoff_idx = i

# 做平滑（显示时使用）
mot_values_pct_s = smooth_list(mot_values_pct, sigma=1.5)
mot_values_col_s = smooth_list(mot_values_col, sigma=1.5)

# === Step 3: 可视化 ===
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# 子图1：原图 + 标注线
axes[0].imshow(img, cmap='gray')
axes[0].set_title("Original Image with Wedge ROI")

# 画出 ROI 区域
axes[0].add_patch(plt.Rectangle((x1, y1), x2-x1, y2-y1,
                                edgecolor='lime', facecolor='none', linewidth=1.5))

# # 若找到了截止频率，则在图上标出对应位置
# if cutoff_idx is not None:
#     cutoff_x = x2 - cutoff_idx * section_width  # 注意翻转
#     axes[0].axvline(x=cutoff_x, color='red', linestyle='--', label=f"MTF≈{MTF_THRESHOLD}")
#     axes[0].legend()

# 子图2：MOT 曲线图
# axes[1].plot(frequencies, mot_values, marker='o')
axes[1].plot(frequencies, mot_values_raw, label='raw min/max', alpha=0.4, marker='o')
axes[1].plot(frequencies, mot_values_pct, label='percentile 5/95', alpha=0.6, marker='o')
axes[1].plot(frequencies, mot_values_pct_s, label='percentile smoothed', linewidth=2)
axes[1].plot(frequencies, mot_values_col_s, label='col-average smoothed', linewidth=2)
axes[1].axhline(MTF_THRESHOLD, color='red', linestyle='--', label=f'MTF={MTF_THRESHOLD} Cutoff')
axes[1].set_xlabel("TV Lines")
axes[1].set_ylabel("MOT (Local Contrast)")
axes[1].set_title("MTF Estimation Curve")
axes[1].grid(True)
axes[1].legend()

# xticks = axes[1].get_xticks()   # 先取原来的刻度位置
# axes[1].set_xticklabels(xticks[::-1].astype(int))  # 倒序显示刻度标签

plt.tight_layout()

# === Step 4: 控制台输出 ===
if cutoff_idx is not None:
    limit_tv = frequencies[cutoff_idx]
    print(f"📏 估计极限分辨率 (MTF≈{MTF_THRESHOLD}): TV ≈ {limit_tv:.2f}")
else:
    print(f"⚠ 所有 MOT 值都大于 {MTF_THRESHOLD}，图像非常清晰，未找到极限分辨率")

plt.show()



# 从左到右的边界
# import cv2
# import numpy as np
# import matplotlib.pyplot as plt

# # === Step 1: 读取图像 ===
# img = cv2.imread('./tools/dingwei.jpg', cv2.IMREAD_GRAYSCALE)
# roi = img[1837:1957, 2059:2525]  # 选定楔形区域
# height, width = roi.shape
# print(f"ROI Size: {height}x{width}")

# _, mask = cv2.threshold(roi, 100, 255, cv2.THRESH_BINARY_INV)


# ys, xs = np.where(mask > 0)   # 取所有前景像素坐标
# x_left, x_right = xs.min(), xs.max()
# y_top, y_bottom = ys.min(), ys.max()
# print(f"楔形最左边: {x_left}, 最右边: {x_right}")


# # === Step 4: 可视化 ===
# plt.imshow(roi, cmap='gray')
# plt.axvline(x_left, color='red', linestyle='--', label='Left')
# plt.axvline(x_right, color='blue', linestyle='--', label='Right')
# plt.axhline(y_top, color='red', linestyle='--', label='Top')
# plt.axhline(y_bottom, color='blue', linestyle='--', label='Bottom')
# plt.legend()
# plt.title("ROI with Left/Right Boundaries")
# plt.axis('off')
# plt.show()