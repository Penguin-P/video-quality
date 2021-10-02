import cv2
import numpy as np
from noise import *

class FrameFuncs(object):
    def __init__(self, frame):
        self.frame = frame

    # ===信号丢失===
    def signalLost(self, thred=0.8):
        # 中值滤波，去噪
        img = cv2.medianBlur(self.frame, 3)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 阈值分割得到二值化图片
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # 膨胀操作
        kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        bin_clo = cv2.dilate(binary, kernel2, iterations=2)
        # 连通域分析
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(bin_clo, connectivity=8)
        ratio = stats[:, 4].max() / stats[:, 4].sum()
        if ratio > thred:
            # text = 'signal: lost'
            text = "1"
        else:
            # text = 'signal: normal'
            text = "0"
        return text


    # ===遮挡===
    def occlusion(self, thred=5):
        # 超过5%认为遮挡
        image = self.frame
        # 创建一个图层 找所有黑色像素点
        # 黑像素点转换成白色
        mask = np.zeros(image.shape, dtype=np.uint8)
        mask[np.where((image <= [15, 15, 15]).all(axis=2))] = [255, 255, 255]

        # Count number of white pixels on mask and calculate percentage
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        h, w = image.shape[:2]
        percentage = (cv2.countNonZero(mask) / (w * h)) * 100
        if percentage < thred:
            # return (percentage, False)
            text = "0"
        else:
            # return (percentage, True)
            text = "1"
        return text


    # ===模糊===
    def blurry(self, thred=800):
        x = cv2.Sobel(self.frame, cv2.CV_16S, 1, 0)
        y = cv2.Sobel(self.frame, cv2.CV_16S, 0, 1)
        absX = cv2.convertScaleAbs(x)
        absY = cv2.convertScaleAbs(y)
        dst = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
        if dst.var() > thred:
            # text = "not blurry"
            text = "0"
        else:
            # text = "blurry"
            text = "1"
        return text

    # ===亮度异常===
    def lumos(self, thred=None):
        # 把图片转换为单通道的灰度图
        gray_img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        # 获取形状以及长宽
        img_shape = gray_img.shape
        height, width = img_shape[0], img_shape[1]
        size = gray_img.size
        # 灰度图的直方图
        hist = cv2.calcHist([gray_img], [0], None, [256], [0, 256])
        # 计算灰度图像素点偏离均值(128)程序
        a = 0
        ma = 0
        # np.full 构造一个数组，用指定值填充其元素
        reduce_matrix = np.full((height, width), 128)
        shift_value = gray_img - reduce_matrix
        shift_sum = np.sum(shift_value)
        da = shift_sum / size
        # 计算偏离128的平均偏差
        for i in range(256):
            ma += (abs(i - 128 - da) * hist[i])
        m = abs(ma / size)
        # 亮度系数
        k = abs(da) / m
        if k[0] > 1:
            # 过亮
            if da > 0:
                # text = 'brightness test: too bright'
                text = "1"
            else:
                # text = 'brightness test: too dark'
                text = "1"
        else:
            # text = 'brightness test: normal'
            text = "0"
        return text

    # ===噪声===
    def noise(self, thred=0.04):
        return saltnoise_check_main(self.frame, thred)

    # ===条纹===
    def ripple(self, thred=0.004):
        img_hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
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
        if streak_rate > thred:
            # text = 'ripple test: abnormal'
            text = "1"
        else:
            # text = 'ripple test: normal'
            text = "0"
        return text

    # ===偏色===
    def colorCast(self, thred=1.5):
        img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2LAB)
        l_channel, a_channel, b_channel = cv2.split(img)
        h, w, _ = img.shape
        da = a_channel.sum() / (h * w) - 128
        db = b_channel.sum() / (h * w) - 128
        histA = [0] * 256
        histB = [0] * 256
        for i in range(h):
            for j in range(w):
                ta = a_channel[i][j]
                tb = b_channel[i][j]
                histA[ta] += 1
                histB[tb] += 1
        msqA = 0
        msqB = 0
        for y in range(256):
            msqA += float(abs(y - 128 - da)) * histA[y] / (w * h)
            msqB += float(abs(y - 128 - db)) * histB[y] / (w * h)
        import math
        result = math.sqrt(da * da + db * db) / math.sqrt(msqA * msqA + msqB * msqB)
        if result > thred:
            text = 'color cast test: abnormal'
        else:
            text = 'color cast test: normal'
        return text

class CompareFuncs(object):
    def __init__(self, oldframe, nowframe):
        self.oldframe = oldframe
        self.nowframe = nowframe

    def freeze(self):
        oldimg = self.oldframe
        nowimg = self.nowframe
        # 假设同一像素位置的变化范围为10
        t = 10
        oldpil = cv2.cvtColor(oldimg, cv2.COLOR_BGR2GRAY)  # PIL图像和cv2图像转化
        nowpil = cv2.cvtColor(nowimg, cv2.COLOR_BGR2GRAY)
        reduce = oldpil - nowpil
        # 将小于t的值取出，并统计数量
        mask = (reduce < t)
        targe_different = reduce[mask]
        different_sum = targe_different.size
        size = oldpil.size
        k = different_sum / size
        # print("图像相同率", k)
        if k > 0.95:
            # print("图像冻结")
            text = "1"
        else:
            # print("图像未冻结")
            text = "0"
        return text




