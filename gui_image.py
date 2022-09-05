import PySimpleGUI as sg
import sys


def create_layout():
    font = ("游明朝", 14)
    sg.theme("GreenMono")
    setting = [
        [__text_temp("インターバル : ", font),
         __time_input_text_temp("interval", font, default_text="1"),
         __text_temp("秒", font)],
    ]
    layout = [
        [sg.Frame("設定", setting, font=font, pad=[(10, 10), (10, 0)])],
        [sg.Button("START", font=font, pad=((40, 10), (10, 10))),
         sg.Button("STOP", font=font, pad=((40, 10), (10, 10)))]
    ]
    return layout


def __time_input_text_temp(key, font, default_text=""):
    return sg.InputText(
        size=(3, 1),
        justification="right",
        key=key,
        font=font,
        default_text=default_text
    )


def __text_temp(text, font):
    return sg.Text(
        text=text,
        font=font
    )


def display():
    window = sg.Window("タイマネ", create_layout())
    while True:
        event, values = window.read()
        if event == "START":
            print("hoge")

        elif event == "STOP":
            print("fuga")

        elif event == sg.WIN_CLOSED:
            window.close()
            sys.exit()


if __name__ == "__main__":
    display()
