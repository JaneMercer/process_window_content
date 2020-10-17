from capture_window import get_window, get_image_

exe_name = 'Discord.exe'  # it is Case sensitive

run = 1
wrong_pids = []
while (run):
    print("Trying to find a window..")
    curr_window_hwnd, wrong_pids = get_window(exe_name, wrong_pids)  # curr_window - will be shown
                                                        # wrong_pids - list of pocessed PIDs with no window to show
    if curr_window_hwnd:
        # print("|DEBUG| wrong_pids: ",wrong_pids)
        # print("|DEBUG| curr_window_hwnd: ", curr_window_hwnd)
        print("PID: ", wrong_pids[-1])
        print("----Window was found!---- \n | Press ESC to shut down the script. \n | Press ENTER to find the next window.\n_______________\n")
        run = get_image_(curr_window_hwnd)
    else:
        print("Sorry, No window was found")
        run = 0
#heeeyoo