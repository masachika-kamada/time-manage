import os
import time
import datetime
import threading
import sys
import PySimpleGUI as sg
import win32gui
import win32process
import psutil
import csv
import matplotlib.pyplot as plt
from gui import create_layout
from visualize import show_result


# スレッド処理のクラス
class Recorder():
    dir_ref = "./timane_csvdata"

    def __init__(self):  # 初期化
        self.ROOP = False  # ループのフラグ
        if not os.path.exists(self.dir_ref):
            os.mkdir(self.dir_ref)

    # ループ処理関数
    def __target(self):
        prev = ""
        fname = self.dir_ref + datetime.datetime.now().strftime("/%Y%m%d.csv")
        while self.ROOP:
            win_name = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if win_name != prev:
                prev = win_name
                pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
                exe_name = psutil.Process(pid[-1]).name()
                with open(fname, mode="a", newline="", encoding="shift-jis", errors="ignore") as f:
                    writer = csv.writer(f)
                    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                    writer.writerow([now, win_name, exe_name])
            time.sleep(self.INTERVAL)

    # スレッドをスタートさせる
    def __start(self):
        if threading.active_count() == 1:
            self.thread = threading.Thread(target=self.__target)
            self.thread.start()

    def startEvent(self, interval):  # STARTボタン押下時の処理
        print("=== START ===")
        self.ROOP = True
        self.INTERVAL = int(interval)
        self.__start()

    def finishEvent(self):  # STOPボタン押下処理
        print("=== STOP ===")
        self.ROOP = False  # ループ停止->自動的にスレッド破棄


def main():
    # スレッド処理のインスタンス生成
    r = Recorder()
    is_running = False
    start_time = 0

    # ウインドウの表示、設定
    window = sg.Window("タイマネ", create_layout(), finalize=True)

    while True:

        event, values = window.read(timeout=10)

        # ボタンの処理内容
        if event == "START / STOP":
            is_running = not is_running
            if is_running:
                r.startEvent(values["interval"])
                start_time = datetime.datetime.now()
            else:
                r.finishEvent()

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
            r.finishEvent()
            window.close()
            sys.exit()

        # タイマーの表示
        if is_running:
            now = datetime.datetime.now()
            elapsed_time = now - start_time
            h = elapsed_time.seconds // 3600
            m = elapsed_time.seconds % 3600 // 60
            s = elapsed_time.seconds % 60
            window["-OUTPUT-"].update(f"{h:02d}:{m:02d}:{s:02d}")


if __name__ == "__main__":
    main()
