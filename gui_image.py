import PySimpleGUI as sg
import sys
import time


class GUI:
    font = ("游明朝", 14)
    input_text_size = (2, 1)

    def __init__(self):
        sg.theme("GreenMono")
        setting = [
            [self.text_temp("インターバル : "),
             self.time_input_text_temp("interval", default_text="1"),
             self.text_temp("秒")],
        ]
        self.layout = [
            [sg.Frame("設定", setting, font=self.font, pad=[(10, 10), (10, 0)])],
            [sg.Button("START", font=self.font, pad=((40, 10), (10, 10))),
             sg.Button("STOP", font=self.font, pad=((40, 10), (10, 10)))]
        ]

    def time_input_text_temp(self, key, default_text=""):
        return sg.InputText(
            size=(3, 1),
            justification='right',
            font=self.font,
            key=key,
            default_text=default_text
        )

    def text_temp(self, text):
        return sg.Text(
            text=text,
            font=self.font
        )

    def display(self):
        window = sg.Window("タイマネ", self.layout)
        while True:
            event, values = window.read()
            if event == "START":
                while event == "START":
                    event, values = window.read(timeout=1000)
                    print("hoge")
                    time.sleep(1)

            elif event == "STOP":
                print("fuga")

            elif event == sg.WIN_CLOSED:
                window.close()
                sys.exit()


if __name__ == "__main__":
    gui = GUI()
    gui.display()
