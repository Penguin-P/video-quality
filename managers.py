import cv2
import time

class CaptureManager(object):
    def __init__(self, inputPath, outputPath, previewWindowManager=None):

        self.previewWindowManager = previewWindowManager

        self._inputPath = inputPath
        self._outputPath = outputPath

        self._capture = cv2.VideoCapture(self.inputPath)
        self._enteredFrame = False
        self._frame = None
        self._videoWriter = None
        self._videoEncoding = None

        self._startTime = None
        self._framesElapsed = 0
        self._fpsEstimate = None

    @property
    def inputPath(self):
        return self._inputPath

    @inputPath.setter
    def inputPath(self, path):
        self._inputPath = path

    @property
    def outputPath(self):
        return self._outputPath

    @outputPath.setter
    def outputPath(self, path):
        self._outputPath = path

    @property
    def frame(self):
        if self._enteredFrame and self._frame is None:
            _, self._frame = self._capture.retrieve()
        return self._frame

    @frame.setter
    def frame(self, img):
        self._frame = img

    @property
    def isWritingVideo(self):
        return self._outputPath is not None

    def enterFrame(self):
        """capture the next frame, if there is any."""
        # first, check that any previous frame was exited.
        assert not self._enteredFrame, \
            'previous enteredFrame() had  no matching exitFrame()'
        if self._capture is not None:
            self._enteredFrame = self._capture.grab()

    def exitFrame(self):
        """draw to window and write to file"""

        #check whether the grabbed frame os retrieveable
        if self.frame is None:
            self._enteredFrame = False
            return

        # update FPS estimate
        if self._framesElapsed == 0:
            self._startTime = time.time()
        else:
            timeElapsed = time.time() - self._startTime
            self._fpsEstimate = self._framesElapsed / timeElapsed
        self._framesElapsed += 1

        """draw to window, if any"""
        if self.previewWindowManager is not None:
            self.previewWindowManager.show(self.frame)

        """write to the video file, if any"""
        self._writeVideoFrame()

        """release the frame"""
        self._frame = None
        self._enteredFrame = False

    def _writeVideoFrame(self):
        if not self.isWritingVideo:
            return

        if self._videoWriter is None:
            fps = self._capture.get(cv2.CAP_PROP_FPS)
            if fps <= 0.0:
                if self._framesElapsed < 20:
                    return
                else:
                    fps = self._fpsEstimate
            size = (int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self._videoWriter = cv2.VideoWriter(
                self._outputPath, self._videoEncoding,
                fps, size
            )

        self._videoWriter.write(self._frame)

class WindowManager(object):

    def __init__(self, windowName, keypressCallback=None):
        self.keypressCallback = keypressCallback

        self._windowName = windowName
        self._isWindowCreated = False

    @property
    def isWindowCreated(self):
        return self._isWindowCreated

    def createWindow(self):
        cv2.namedWindow(self._windowName)
        self._isWindowCreated = True

    def show(self, frame):
        cv2.imshow(self._windowName, frame)

    def destroyWindow(self):
        cv2.destroyWindow(self._windowName)
        self._isWindowCreated = False

    def processEvents(self):
        keycode = cv2.waitKey(1)
        if self.keypressCallback is not None and keycode != -1:
            # Discard any non-ASCII info encoded by GTK.
            keycode &= 0xFF
            self.keypressCallback(keycode)