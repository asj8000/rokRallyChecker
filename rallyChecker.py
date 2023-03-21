import cv2
import numpy as np
import time
import win32gui
import pyautogui
import datetime
import pytesseract

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

        return cv2.cvtColor(
            np.asarray(
                pyautogui.screenshot(
                    region=(x, y,
                            *win32gui.ClientToScreen(hwnd, (right - x, bot - y))))), cv2.COLOR_RGB2BGR)


# 랠리 팝업 탬플릿
rallyPopupTemplate = cv2.imread('C:/development/project/rokRallyChecker/rallyPopupTemplate.png',cv2.IMREAD_GRAYSCALE)

def checkIsRally(frame):
    """
    이미지 체킹 로직. 이미지 내에서 템플릿 이미지 여부 확인.
    :param frame:
    :return:
    """
    # 가져온 프레임 그레이 스케일 처리
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 탬플릿 매칭 해내기
    res = cv2.matchTemplate(gray_frame, rallyPopupTemplate, cv2.TM_CCOEFF_NORMED)
    # 임계치 정하기
    threshold = .65
    #임계치 이상만 배열에 저장
    loc = np.where(res >= threshold)
    if loc[0].size != 0 and loc[1].size != 0:
        print("RallyPopupTemplate Found!")
        return True
    else:
        return False

def saveFrame(frame):
    """
    이미지 저장 함수. 테스트 파일 체킹용으로 씀. 개발후엔 삭제.
    :param frame:
    :return:
    """
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")

    cv2.imwrite(timestamp+'.jpg', frame)


ESC_KEY=27
FRAME_RATE = 1
SLEEP_TIME = 1/FRAME_RATE

# 스크린샷 대상 인식
capture = WindowCapture("라이즈 오브 킹덤즈",FRAME_RATE)

while True:
    start=time.time()
    # 해당 앱 스크린샷 떠서 이미지 얻어옴.
    frame = capture.screenshot()

    cv2.imshow("frame1",frame)

    if(checkIsRally(frame)):
        saveFrame(frame)
        time.sleep(2)
        ## 존재 여부 확인하였을 경우
        ## 해당 영역에서 글자 인식 (영어, 한글, 일본어, 중국어, 특수문자 등등 전부 인식 필요), tesseract 셋업 먼저 고고
        ## 스프레드 시트에 차곡차곡 적재 로직 추가

    delta= time.time()-start
    if delta <SLEEP_TIME:
        time.sleep(SLEEP_TIME-delta)
    key= cv2.waitKey(1) & 0xFF
    if key== ESC_KEY:
        break

cv2.destroyAllWindows()