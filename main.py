import time
import datetime
import threading
import sys
import PySimpleGUI as sg
import win32gui
import win32process
import psutil
import csv
from gui import create_layout


# スレッド処理のクラス
class Recorder():
    def __init__(self):  # 初期化
        self.ROOP = False  # ループのフラグ

    # ループ処理関数
    def __target(self):
        prev = ""
        fname = datetime.datetime.now().strftime("timane-%Y%m%d.csv")
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

    # ウインドウの表示、設定
    window = sg.Window("タイマネ", create_layout(), finalize=True)

    while True:

        event, values = window.read()

        # ボタンの処理内容
        if event == "START":
            r.startEvent(values["interval"])

        elif event == "STOP":
            r.finishEvent()

        elif event is None:
            r.finishEvent()
            window.close()
            sys.exit()


if __name__ == "__main__":
    main()
