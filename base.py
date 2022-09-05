import time
import threading
import sys
import PySimpleGUI as sg


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
    sg.theme("BluePurple")
    layout = [[sg.Text("処理の実行、変更、停止を行います:"), sg.Text(size=(15, 1), key="-OUTPUT-")],
              [sg.Button("Start"), sg.Button("Change"), sg.Button("Stop")]]
    window = sg.Window("Pattern 2B", layout)

    while True:

        event, values = window.read()
        print(event, values)

        # ボタンの処理内容
        if event == "Start":
            window["-OUTPUT-"].update("実行中")
            startEvent(r)

        elif event == "Change":
            window["-OUTPUT-"].update("変更しました")
            changeEvent(r)

        elif event == "Stop":
            finishEvent(r)

        elif event is None:
            finishEvent(r)
            window.close()  # ウインドウを消す
            sys.exit()  # アプリ終了


if __name__ == "__main__":
    main()
