import cv2
import os
import errno
import json
from managers import WindowManager, CaptureManager
from estimate import FrameFuncs, CompareFuncs
import argparse



def parse_args():
    parser = argparse.ArgumentParser(description='Estimate Video Quality')
    parser.add_argument('--input', help='video input path', dest='input', type=str)
    parser.add_argument('--output', help='video output path', dest='output', type=str)
    # parser.add_argument('--method', help='0 for blurrytest, 1 for ripple, 2 for brightness test, 3 for color cast test, 4 for signal test, 5 for salt peper noise test', dest='method', default=0, type=int)
    # parser.add_argument('--thred', help='threshold', dest='thred', type=float)
    args = parser.parse_args()
    return args

class est(object):
    def __init__(self):
        self._id = int(0)
        self._name = str(0)
        self._inputPath = parse_args().input
        self._outputPath = parse_args().output

        self._windowManager = WindowManager('estimate',
                                            self.onKeypress)
        self._captureManager = CaptureManager(
            inputPath=self._inputPath, outputPath=self._outputPath, previewWindowManager=self._windowManager
        )

    def run(self):
        # method = parse_args().method
        # thred = parse_args().thred
        """run the main loop"""
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame
            self._captureManager.exitFrame()
            self._captureManager.enterFrame()
            nowframe = self._captureManager.frame
            if (frame is not None) and (nowframe is not None):
                Frame = FrameFuncs(frame)
                CopFrame = CompareFuncs(frame, nowframe)
                # if method == 0:
                # self._captureManager.frame = cv2.putText(frame, Frame.blurry(), (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                #                                              0.8, (255, 0, 0), 2)
                # elif method == 1:
                #     self._captureManager.frame = cv2.putText(frame, Frame.ripple(thred), (10, 60),
                #                                              cv2.FONT_HERSHEY_SIMPLEX,
                #                                              0.8, (255, 0, 0), 2)
                # elif method == 2:
                #     self._captureManager.frame = cv2.putText(frame, Frame.lumos(thred), (10, 60),
                #                                              cv2.FONT_HERSHEY_SIMPLEX,
                #                                              0.8, (255, 0, 0), 2)
                # elif method == 3:
                #     self._captureManager.frame = cv2.putText(frame, Frame.colorCast(thred), (10, 60),
                #                                              cv2.FONT_HERSHEY_SIMPLEX,
                #                                              0.8, (255, 0, 0), 2)
                #
                # elif method == 4:
                #     self._captureManager.frame = cv2.putText(frame, Frame.signalLost(thred), (10, 60),
                #                                              cv2.FONT_HERSHEY_SIMPLEX,
                #                                              0.8, (255, 0, 0), 2)
                #
                # elif method == 5:
                #     self._captureManager.frame = cv2.putText(frame, Frame.noise(thred), (10, 60),
                #                                              cv2.FONT_HERSHEY_SIMPLEX,
                #                                              0.8, (255, 0, 0), 2)
                id = self._id
                name = self._name
                operate = ["0", Frame.signalLost(), Frame.occlusion(), Frame.blurry(), Frame.lumos(), CopFrame.freeze(), Frame.noise(), Frame.ripple()]
                status = "".join(operate)
                dict = {"id": id, "name": name, "status": status}
                # print(status, id)
                js_res = json.dumps(dict, sort_keys=True, indent=2, separators=(", ", ": "))
                print(js_res)
            self._captureManager.exitFrame()
            self._windowManager.processEvents()
            if frame is None:
                id = self._id
                name = self._name
                status = "111111111"
                dict = {"id": id, "name": name, "status": status}
                js_res = json.dumps(dict, sort_keys=True, indent=2, separators=(", ", ": "))
                print(js_res)


    def onKeypress(self, keycode):
        if keycode == 27:
            self._windowManager.destroyWindow()


if __name__=="__main__":
    Video = est()
    Video.run()