import cv2
import argparse
import os


def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='Process pic')
    parser.add_argument('--input', help='video to process', dest='input', type=str)
    parser.add_argument('--output', help='pic to store', dest='output', type=str)
    # default为间隔多少帧截取一张图片
    parser.add_argument('--skip-frame', help='skip number of video', dest='skip_frame', default=25, type=int)
    # input为输入视频的路径 ，output为输出存放图片的路径
    args = parser.parse_args()
    return args


def process_video(i_video, o_video, num):
    cap = cv2.VideoCapture(i_video)
    num_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    expand_name = '.jpg'
    if not cap.isOpened():
        print("Please check the path.")
    cnt = 0
    count = 0
    while True:
        flag, frame = cap.read()
        if not flag:
            break
        cnt += 1
        if cnt % num == 0:
            cv2.imwrite(os.path.join(o_video, str(count) + expand_name), frame)
            count += 1


if __name__ == '__main__':
    args = parse_args()
    os.makedirs(args.output, exist_ok=True)
    print('Called with args:')
    print(args)
    process_video(args.input, args.output, args.skip_frame)
