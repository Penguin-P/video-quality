import time
import multiprocessing as mp
import cv2


def image_put(q):
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print('OPENED')

    while True:
        q.put(cap.read()[1])
        q.get() if q.qsize() > 1 else time.sleep(0.01)


def image_get(q, window_name="window1"):
    cv2.namedWindow(window_name, flags=cv2.WINDOW_FREERATIO)
    while True:
        frame = q.get()
        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


def run_single_camera():
    mp.set_start_method(method='spawn')  # init
    queue = mp.Queue(maxsize=2)

    processes = [mp.Process(target=image_put, args=(queue,)),
                 mp.Process(target=image_get, args=(queue,))]

    [process.start() for process in processes]
    [process.join() for process in processes]


def run():
    run_single_camera()  # quick, with 2 threads


if __name__ == "__main__":
    run()
