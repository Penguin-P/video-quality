import cv2
import numpy as np

# sobel 算子
# 0度(水平)方向
sobel_1 = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]])
# 90度(垂直)方向
sobel_2 = np.array([[-1, -2, -1],
                    [0, 0, 0],
                    [1, 2, 1]])
# 135
sobel_3 = np.array([[0, 1, 2],
                    [-1, 0, 1],
                    [-2, -1, 0]])
# 45
sobel_4 = np.array([[-2, -1, 0],
                    [-1, 0, 1],
                    [0, 1, 2]])
# # prewitt 算子
# prewitt_1 = np.array([[-1, 0, 1],
#                       [-1, 0, 1],
#                       [-1, 0, 1]])
#
# prewitt_2 = np.array([[-1, -1, -1],
#                       [0, 0, 0],
#                       [1, 1, 1]])


# 卷积
def imgConvolve(image, kernel):
    '''
    :param image: 图片矩阵
    :param kernel: 滤波窗口
    :return:卷积后的矩阵
    '''
    img_h = int(image.shape[0])
    img_w = int(image.shape[1])
    kernel_h = int(kernel.shape[0])
    kernel_w = int(kernel.shape[1])
    # padding
    padding_h = int((kernel_h - 1) / 2)
    padding_w = int((kernel_w - 1) / 2)

    convolve_h = int(img_h + 2 * padding_h)
    convolve_W = int(img_w + 2 * padding_w)

    # 分配空间
    img_padding = np.zeros((convolve_h, convolve_W))
    # 中心填充图片
    img_padding[padding_h:padding_h + img_h, padding_w:padding_w + img_w] = image[:, :]
    # 卷积结果
    image_convolve = np.zeros(image.shape)
    # 卷积
    for i in range(padding_h, padding_h + img_h):
        for j in range(padding_w, padding_w + img_w):
            image_convolve[i - padding_h][j - padding_w] = int(
                np.sum(img_padding[i - padding_h:i + padding_h + 1, j - padding_w:j + padding_w + 1] * kernel))

    return image_convolve


# Sobel Edge
def sobelEdge(image, sobel):
    '''
    :param image: 图片矩阵
    :param sobel: 滤波窗口
    :return:Sobel处理后的矩阵
    '''
    return imgConvolve(image, sobel)


def saltnoise_check_main(image, thred=0.04):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    r, c = image.shape[:2]
    piexs_sum = r * c
    # img_spbel1 = sobelEdge(image, sobel_1)
    # img_spbel2 = sobelEdge(image, sobel_2)
    # img_spbel3 = sobelEdge(image, sobel_3)
    # img_spbel4 = sobelEdge(image, sobel_4)
    #
    img_spbel1 = cv2.filter2D(image, -1, sobel_1)
    img_spbel2 = cv2.filter2D(image, -1, sobel_2)
    img_spbel3 = cv2.filter2D(image, -1, sobel_3)
    img_spbel4 = cv2.filter2D(image, -1, sobel_4)
    #
    img_spbel1_abs = abs(img_spbel1)
    img_spbel2_abs = abs(img_spbel2)
    img_spbel3_abs = abs(img_spbel3)
    img_spbel4_abs = abs(img_spbel4)

    # 将所有矩阵大于0.1的位置提取出来，并且转换成0 1进行点乘，即可算出4个矩阵均大于0.1的位置
    img_spbel1_locate = (img_spbel1_abs > 0.1) + 0
    img_spbel2_locate = (img_spbel2_abs > 0.1) + 0
    img_spbel3_locate = (img_spbel3_abs > 0.1) + 0
    img_spbel4_locate = (img_spbel4_abs > 0.1) + 0

    count_locate = img_spbel1_locate * img_spbel2_locate * img_spbel3_locate * img_spbel4_locate

    # 中值滤波
    lbimg = cv2.medianBlur(image, 3)
    # 计算abs(灰度图-中值滤波) > 30 且 卷积绝对值最小值大于0.1的
    reduce = abs(lbimg - image) * count_locate

    noise_point = reduce[reduce > 30]
    noise_point_num = noise_point.size
    noise_rate = noise_point_num / piexs_sum
    if noise_rate > thred:
        # text = 'noise test: noisy'
        text = "1"
    else:
        # text = 'noise test: normal'
        text = "0"
    return text


if __name__ == '__main__':
    img = cv2.imread('./frame_imgs/83雪花无信号/0.jpg')
#     img = cv2.imread('./oth_imgs/zelda0.png', cv2.IMREAD_GRAYSCALE)
    print(saltnoise_check_main(img))
