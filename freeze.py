import cv2
oldimg = cv2.imread('./oth_imgs/test.jpg')
nowimg = cv2.imread('./oth_imgs/test.jpg')
# 假设同一像素位置的变化范围为10
t = 10

oldpil = cv2.cvtColor(oldimg, cv2.COLOR_BGR2GRAY)   # PIL图像和cv2图像转化
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
    print("图像冻结")
else:
    print("图像未冻结")