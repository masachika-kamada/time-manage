import time
import threading
import sys
import PySimpleGUI as sg
from gui_image import create_layout
import win32gui
import win32process
import psutil


# スレッド処理のクラス
class Receive():
    def __init__(self):  # 初期化
        self.ROOP = False  # ループのフラグ

    # ループ処理関数
    def target(self):
        while (self.ROOP):  # ループする処理
            win_name = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            print(win_name)
            pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
            exe_name = psutil.Process(pid[-1]).name()
            print(exe_name)
            time.sleep(self.INTERVAL)

    # スレッドをスタートさせる
    def start(self):
        if threading.active_count() == 1:
            self.thread = threading.Thread(target=self.target)
            self.thread.start()


def startEvent(r, interval):  # STARTボタン押下時の処理
    r.ROOP = True
    r.INTERVAL = int(interval)
    r.start()


def finishEvent(r):  # STOPボタン押下処理
    print("終了しました")
    r.ROOP = False  # ループ停止->自動的にスレッド破棄


def main():
    # スレッド処理のインスタンス生成
    r = Receive()

    # ウインドウの表示、設定
    window = sg.Window("タイマネ", create_layout(), finalize=True)

    while True:

        event, values = window.read()
        print(event, values)

        # ボタンの処理内容
        if event == "START":
            startEvent(r, values["interval"])

        elif event == "STOP":
            finishEvent(r)

        elif event is None:
            finishEvent(r)
            window.close()
            sys.exit()


if __name__ == "__main__":
    main()
