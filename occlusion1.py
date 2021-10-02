import cv2
import numpy as np

def detect_occluded(image, threshold=5):
    # 超过5%认为遮挡

    # 创建一个图层 找所有黑色像素点
    # 黑像素点转换成白色
    mask = np.zeros(image.shape, dtype=np.uint8)
    mask[np.where((image <= [15,15,15]).all(axis=2))] = [255,255,255]

    # Count number of white pixels on mask and calculate percentage
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    h, w = image.shape[:2]
    percentage = (cv2.countNonZero(mask)/ (w * h)) * 100
    if percentage < threshold:
        # return (percentage, False)
        text = "0"
    else:
        # return (percentage, True)
        text = "1"
    return text


if __name__ == "__main__":
    image = cv2.imread('./oth_imgs/test.jpg')
    percentage, occluded = detect_occluded(image)
    print('Pixel Percentage: {:.2f}%'.format(percentage))
    print('Occluded:', occluded)