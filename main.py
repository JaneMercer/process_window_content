from capture_window import get_image_, get_window

exe_name = 'Telegram.exe'  # Name of the process for which this script will search for windows
# run = 1  # bool - should the program continue to search
wrong_pids = []  # list of processed PIDs with no window to show or/and windows that were already shown
prev_foundPIDs = []

print("Trying to find a window..")
window_HWNDs, all_PIDs = get_window(exe_name)  # tries to find a new window handle by process name

if window_HWNDs:  # if window handle was found
    print("All process PID: ", all_PIDs)  # writes a PID of the windows that will be shown
    print("All window HWNDs: ", window_HWNDs)
    print("----Window was found!---- \n "
          "| Press ESC to shut down the script. \n "
          "| Press ENTER to find the next window.\n_______________\n")
    for curr_window_hwnd in window_HWNDs:
        run = get_image_(curr_window_hwnd)  # gets the image from this window to show
        if not run: break

else:
    print("Sorry, No window was found")
    run = 0

