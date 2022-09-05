import time
import threading
import sys
import PySimpleGUI as sg
from gui_image import create_layout


# スレッド処理のクラス
class Receive():
    def __init__(self):  # 初期化
        self.ROOP = False  # ループのフラグ
        self.num = 1

    # ループ処理関数
    def target(self):
        while (self.ROOP):
            # ここにループする処理を記載
            print("number : ", self.num)
            time.sleep(1)  # 1秒待機

    # スレッドをスタートさせる
    def start(self):
        if threading.active_count() == 1:
            self.thread = threading.Thread(target=self.target)
            self.thread.start()


def startEvent(r):  # スタートボタン押下時の処理
    r.ROOP = True
    r.start()


def changeEvent(r):  # 接続変更ボタン押下時の処理
    r.num = r.num + 1


def finishEvent(r):  # 終了ボタン押下処理
    print("終了しました")
    r.ROOP = False  # ループ停止　-> 自動的にスレッド破棄


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
            startEvent(r)

        elif event == "STOP":
            finishEvent(r)

        elif event is None:
            finishEvent(r)
            window.close()  # ウインドウを消す
            sys.exit()  # アプリ終了


if __name__ == "__main__":
    main()
