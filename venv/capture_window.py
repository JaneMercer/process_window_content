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


def get_window(w_name, wrong_processes):
    try:
        windows = []
        instansess = [item for item in psutil.process_iter() if item.name() == w_name]
        # print(instansess)
        windows.clear() #TO FIND A NEW WINDOW
        # Просто pid первого попавшегося процесса с именем файла
        if (instansess):
            while not windows:
                pid = next(item for item in psutil.process_iter() if (item.name() == w_name and item.pid not in wrong_processes) ).pid
                # (вызовет исключение StopIteration, если не запущен)
                # print("PID: ", pid)
                win32gui.EnumWindows(enum_window_callback, [pid, windows])
                wrong_processes.append(pid)
            return (windows[0], wrong_processes)
        else:
            # print("Process ", w_name, " was not found.")
            return ([],wrong_processes)

    except Exception as e:
        # if e == 'StopIteration':
            print("No more windows. Bye-bye!")
            return ([],wrong_processes)
        # else: print(e)




def resize(im):
    width = int(im.shape[1] * 30 / 100)
    height = int(im.shape[0] * 30 / 100)
    dsize = (width, height)
    resized = cv2.resize(im, dsize)
    return resized


def process_image(im):
    image2 = resize(im)
    hsl = cv2.cvtColor(image2, cv2.COLOR_BGR2HLS)
    mask = cv2.inRange(hsl, np.array([120,0,40]), np.array([135,40,255]))
    blank_image = image2.copy()
    blank_image[:] = (0, 0, 255)
    res = cv2.bitwise_and(blank_image,blank_image, mask= mask)
    return res
    # return im


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
        return img,result
    else:
        return None,result


def get_image_(window):
    bbox = win32gui.GetWindowRect(window)
    left, top, right, bot = bbox
    w = right - left
    h = bot - top

    if (w > 0 and h > 0):
        try:
            while(1):
                win_img, bool_img = win_create_bitmap(window, w,h)
                if bool_img:  # PrintWindow Succeeded
                    cv_img = cv2.cvtColor(win_img, cv2.COLOR_RGBA2RGB)
                    cv2.imshow('screen',process_image(cv_img))
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