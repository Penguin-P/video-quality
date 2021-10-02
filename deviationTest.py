import numpy as np
import cv2
import deviation
from PIL import Image, ImageDraw, ImageFont

def putText(frame, text):
    cv2_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(cv2_img)

    draw = ImageDraw.Draw(pil_img)
    font = ImageFont.truetype("./fonts/SimHei.ttf", 30, encoding="utf-8")
    draw.text((50,50), text, (0, 255, 255), font=font)

    cv2_text_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    return cv2_text_img

text = ["完全偏移", "严重偏移", "轻微偏移", "无偏移"]

cap = cv2.VideoCapture("./video_src/偏移.mp4")
# cap = cv2.VideoCapture(0)

if (cap.isOpened() == False):
    print("文件或摄像头打开错误")

first_frame = True
pre_frame = 0
index = 0

while (True):
    flag, frame = cap.read()
    if flag == True:
        if first_frame:
            pre_frame = frame
            first_frame = False
            continue

        index += 1
        if index % 14 == 0:
            result = deviation.matchFrames(pre_frame, frame)
            print("检测结果===>", text[result])

            if result > 1:  # 缓存最近无偏移的帧
                pre_frame = frame

            size = frame.shape

            if size[1] > 720:  # 缩小显示
                frame = cv2.resize(frame, (int(size[1] * 0.5), int(size[0] * 0.5)), cv2.INTER_LINEAR)

            text_frame = putText(frame, text[result])

            cv2.imshow('Frame', text_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()