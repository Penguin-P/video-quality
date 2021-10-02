import cv2
import numpy as np

# img = cv2.imread('./frame_imgs/84波纹/0.jpg')
# img = cv2.imread('./frame_imgs/116亮度异常/0.jpg')
img = cv2.imread('./oth_imgs/xilmo1.png')
# img = cv2.imread('./oth_imgs/zelda0.png')  # 可能跟图片的笔触有关

img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
H = cv2.split(img_hsv)[0]

# 傅里叶变换
f = np.fft.fft2(H)
r, c = f.shape
fshift = np.fft.fftshift(f)
# f_img = 20 * np.log(np.abs(f))
magnitude_spectrum = 20 * np.log(np.abs(fshift))
matrix_mean = np.mean(magnitude_spectrum)
# 计算阈值
matrix_std = np.std(magnitude_spectrum)
# 最大值
matrix_max = magnitude_spectrum.max()
# 计算阈值(均值加3倍标准差 和 最大值/2 中大的值为阈值)
T = max(matrix_mean + 3 * matrix_std, matrix_max / 2)
# 将小于T的变为0
# magnitude_spectrum[magnitude_spectrum < T] = 0
# 统计大于T的点数
magnitude_points = (magnitude_spectrum >= T)
target_array = magnitude_spectrum[magnitude_points]
magnitude_sum = target_array.size
streak_rate = magnitude_sum / (c * r)
print("条纹率", streak_rate)
if streak_rate > 0.004:
    print("图片条纹")
else:
    print("图片正常")
