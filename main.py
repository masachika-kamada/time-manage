import os
import time
import datetime
import sys
import PySimpleGUI as sg
import win32gui
import win32process
import psutil
import csv
import matplotlib.pyplot as plt
from gui import create_layout
from visualize import show_result


def finish_event(fname):  # STOPボタン押下処理
    with open(fname, mode="a", newline="", encoding="shift-jis", errors="ignore") as f:
        writer = csv.writer(f)
        now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        writer.writerow([now, "タイマネ", "timane.exe"])
    print("=== STOP ===")


def update_time(elapsed_time):
    h = elapsed_time.seconds // 3600
    m = elapsed_time.seconds % 3600 // 60
    s = elapsed_time.seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


def get_active_window(prev):
    # ウインドウのタイトルを取得
    win_name = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    if win_name != prev:
        pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        if pid[-1] <= 0:  # 例外処理への対応
            return False, None, None
        try:
            exe_name = psutil.Process(pid[-1]).name()
            return True, win_name, exe_name
        except Exception as e:
            pass
    return False, None, None


def main():
    dir_ref = "./timane_csvdata"
    if not os.path.exists(dir_ref):
        os.mkdir(dir_ref)
    fname = dir_ref + datetime.datetime.now().strftime("/%Y%m%d.csv")
    is_running = False
    start_time = 0
    prev = ""
    INTERVAL = 1
    last_time = time.time()

    # ウインドウの表示、設定
    window = sg.Window("タイマネ", create_layout(), finalize=True)

    while True:

        event, values = window.read(timeout=10)

        # ボタンの処理内容
        if event == "START / STOP":
            is_running = not is_running
            if is_running:
                INTERVAL = int(values["interval"])
                start_time = datetime.datetime.now()
                last_time = time.time()
            else:
                finish_event(fname)

        elif event == "実行ファイル / 円グラフ":
            show_result(values["file"], "exe", "pie")

        elif event == "実行ファイル / 表":
            show_result(values["file"], "exe", "table")

        elif event == "閲覧ページ / 円グラフ":
            show_result(values["file"], "page", "pie")

        elif event == "閲覧ページ / 表":
            show_result(values["file"], "page", "table")

        elif event == "実行ファイル / 円グラフ0":
            show_result(values["file1"], "exe", "pie", "user1")
            show_result(values["file2"], "exe", "pie", "user2")
            plt.show()

        elif event == "閲覧ページ / 円グラフ1":
            show_result(values["file1"], "page", "pie", "user1")
            show_result(values["file2"], "page", "pie", "user2")
            plt.show()

        elif event == sg.WIN_CLOSED:
            finish_event(fname)
            window.close()
            sys.exit()

        # タイマーの表示
        if is_running:
            now = datetime.datetime.now()
            window["-OUTPUT-"].update(update_time(now - start_time))

            if time.time() - last_time > INTERVAL:
                last_time = time.time()
                # ウインドウのタイトルを取得
                ret, win_name, exe_name = get_active_window(prev)
                if ret:
                    prev = win_name
                    with open(fname, mode="a", newline="", encoding="shift-jis", errors="ignore") as f:
                        writer = csv.writer(f)
                        now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                        writer.writerow([now, win_name, exe_name])


if __name__ == "__main__":
    main()
