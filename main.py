from capture_window import get_window, get_image_

exe_name = 'Calculator.exe'    # script will search for windows of this process (it is Case sensitive)
run = 1                     # this boolean tells should the program continue to search
wrong_pids = []             # list of processed PIDs with no window to show or/and windows that were already shown


while run:
    print("Trying to find a window..")
    curr_window_hwnd, wrong_pids = get_window(exe_name, wrong_pids)  # tries to find a new window handle by process name

    if curr_window_hwnd: # if window handle was found
        # print("|DEBUG| wrong_pids: ",wrong_pids)
        # print("|DEBUG| curr_window_hwnd: ", curr_window_hwnd)
        print("PID: ", wrong_pids[-1]) # writes a PID of the window that will be shown
        print("----Window was found!---- \n | Press ESC to shut down the script. \n | Press ENTER to find the next window.\n_______________\n")
        run = get_image_(curr_window_hwnd)  # gets the image from this window to show
    else:
        print("Sorry, No window was found")
        run = 0
#heeeyoo