import cv2
import numpy as np
import time
import win32gui
import pyautogui

class WindowCapture:
    def __init__(self,window_name,capture_rate):
        self.window_name = window_name
        self.wait_time = 1/capture_rate

        self.frame=self.screenshot()
    def screenshot(self):
        hwnd = win32gui.FindWindow(None, self.window_name)
        if not hwnd:
            raise Exception('Window not found: ' + self.window_name)

        left, top, right, bot = win32gui.GetClientRect(hwnd)
        x, y = win32gui.ClientToScreen(hwnd, (left, top))
        if(right != 900):
            print(left, top, right, bot)

        return cv2.cvtColor(
            np.asarray(
                pyautogui.screenshot(
                    region=(x, y,
                            *win32gui.ClientToScreen(hwnd, (right - x, bot - y))))), cv2.COLOR_RGB2BGR)



# 랠리 팝업 탬플릿
rallyPopupTemplate = cv2.imread('C:/development/project/rokRallyChecker/rallyPopupTemplate.bmp')


def checkIsRally(frame):
    frame = cv2.imread(frame,cv2.IMREAD_GRAYSCALE)
    # 탬플릿 매칭 해내기
    res = cv2.matchTemplate(frame, rallyPopupTemplate, cv2.TM_CCOEFF_NORMED)
    # 임계치 정하기
    threshold = .65
    #임계치 이상만 배열에 저장
    loc = np.where(res >= threshold)
    if(loc[::-1]):
        print("true!")
        return 1
    return 0


ESC_KEY=27
FRAME_RATE = 0.5
SLEEP_TIME = 1/FRAME_RATE

# 스크린샷 대상 인식
capture = WindowCapture("라이즈 오브 킹덤즈",FRAME_RATE)

while True:
    start=time.time()
    # 해당 앱 스크린샷 떠서 이미지 얻어옴.
    frame = capture.screenshot()

    cv2.imshow("frame1",frame)

    delta= time.time()-start
    if delta <SLEEP_TIME:
        time.sleep(SLEEP_TIME-delta)
    key= cv2.waitKey(1) & 0xFF
    if key== ESC_KEY:
        break

