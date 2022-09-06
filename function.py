import win32process
from win32com.client import GetObject
import win32gui
import time


def get_foreground_window():
    win_name = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    print(win_name)

    hwnd = win32gui.FindWindow(None, win_name)
    threadid, pid = win32process.GetWindowThreadProcessId(hwnd)
    print("pid=" + str(pid))

    try:
        _wmi = GetObject("winmgmts:")

        # collect all the running processes
        processes = _wmi.ExecQuery("Select * from win32_process")
        for p in processes:
            if isinstance(p.ProcessId, int) and p.ProcessId == pid:
                print((p.ProcessId, p.ExecutablePath, p.Name))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    for i in range(10):
        get_foreground_window()
        time.sleep(1)
