import cv2

# img = cv2.imread('./frame_imgs/62清晰度异常/0.jpg', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('./frame_imgs/62清晰度异常/10.jpg', cv2.IMREAD_GRAYSCALE)
img = cv2.imread('./frame_imgs/116亮度异常/0.jpg', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('./frame_imgs/116亮度异常/10.jpg', cv2.IMREAD_GRAYSCALE)

x = cv2.Sobel(img, cv2.CV_16S, 1, 0)
y = cv2.Sobel(img, cv2.CV_16S, 0, 1)

absX = cv2.convertScaleAbs(x)
absY = cv2.convertScaleAbs(y)

dst = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)

print(dst.var())

# 阈值暂定为 1450
if dst.var() > 1450:
    print('清晰度正常')
else:
    print('清晰度异常')

cv2.imshow('absX', absX)
cv2.imshow('absY', absY)
cv2.imshow('result', dst)

cv2.waitKey(0)
# 按任意建关闭窗口
cv2.destroyAllWindows()