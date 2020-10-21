import psutil
import win32gui
import win32ui
import win32process
import ctypes
import numpy as np
import cv2
import time


def enum_window_callback(hwnd, pid_and_windows):
    pid, windows = pid_and_windows
    tid, current_pid = win32process.GetWindowThreadProcessId(hwnd)
    if pid == current_pid:
        windows.append(hwnd)


def get_window(w_name):
    try:
        instansess = [item for item in psutil.process_iter() if item.name() == w_name]
        _PIDs = [item.pid for item in instansess]

        if instansess:
            window_HWNDs = []

            for pid in _PIDs:
                win32gui.EnumWindows(enum_window_callback, [pid, window_HWNDs])

            return (window_HWNDs, _PIDs)
        else:
            print("Process ", w_name, " was not found.")
            return ([], [])

    except Exception as e:
        print(e)
        return ([], [])


def resize(im, coef):  # resizes the image by coef
    MAX_SIZE = 2000
    MIN_SIZE = 10
    width = int(im.shape[1] * coef)
    height = int(im.shape[0] * coef)
    dsize = (width, height)

    if width > MIN_SIZE or height > MIN_SIZE or height < MAX_SIZE or width < MAX_SIZE:
        return cv2.resize(im, dsize)
    else:
        print("Resized image is to small or to big. No resizing was done.")
        return im


def process_image(im):  # processes the image the way you want
    image2 = resize(im, 0.3)
    hsl = cv2.cvtColor(image2, cv2.COLOR_BGR2HLS)
    mask = cv2.inRange(hsl, np.array([120, 0, 40]), np.array([135, 40, 255])) #masks specific color range
    blank_image = image2.copy()
    blank_image[:] = (0, 0, 255)
    res = cv2.bitwise_and(blank_image, blank_image, mask=mask) #applies mask to the image and shows result on black bg
    return res


def win_create_bitmap(window, w, h):
    hwndDC = win32gui.GetWindowDC(window)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    # Change the line below depending on whether you want the whole window
    # or just the client area.
    # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    result = ctypes.windll.user32.PrintWindow(window, saveDC.GetSafeHdc(), 1)
    if result == 1:
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        img = np.fromstring(bmpstr, dtype='uint8')
        img.shape = (h, w, 4)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(window, hwndDC)

    if result:
        return img, result
    else:
        return None, result


def get_image_(window):
    bbox = win32gui.GetWindowRect(window)
    left, top, right, bot = bbox
    w = right - left
    h = bot - top

    if (w > 0 and h > 0):
        try:
            while (1):
                win_img, bool_img = win_create_bitmap(window, w, h)
                if bool_img:  # PrintWindow Succeeded
                    cv_img = cv2.cvtColor(win_img, cv2.COLOR_RGBA2RGB)
                    # cv2.imshow('screen',process_image(cv_img))
                    cv2.imshow('screen', cv_img)
                    time.sleep(1.0 / 10)
                    k = cv2.waitKey(33)
                    if k == 27:  # Esc key to stop
                        print("....Exiting")
                        cv2.destroyWindow('screen')
                        return 0
                    elif k == 13:
                        cv2.destroyWindow('screen')
                        return 1
                    else:
                        continue
                else:
                    print("Problems with PrintWindow")
                    return 1

        except Exception as e:
            print(e)
            return 1
    else:
        print(" ... Ops!Window to small. \n")
        return 1
