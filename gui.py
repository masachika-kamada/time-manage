import PySimpleGUI as sg


def create_layout():
    layout = [
        [sg.TabGroup([[
            sg.Tab("計測", __create_measure(), key='tab1'),
            sg.Tab("可視化", __create_file_select(), key='tab2'),
            sg.Tab("比較・可視化", __create_file_compare(), key='tab3'),
        ]])],
    ]
    return layout


def __create_measure():
    font = ("游明朝", 14)
    sg.theme("GreenMono")
    setting = [
        [__text_temp("インターバル : ", font),
         __time_input_text_temp("interval", font, default_text="1"),
         __text_temp("秒", font)],
    ]
    layout = [
        [sg.Text("00:00:00", font=("游明朝", 34), pad=[(37, 0), (20, 0)], justification="center", key="-OUTPUT-")],
        [sg.Frame("設定", setting, font=font, pad=[(10, 10), (10, 0)])],
        [sg.Button("START / STOP", font=font, pad=((43, 10), (20, 15)))]
    ]
    return layout


def __create_file_select():
    font = ("游明朝", 12)
    sg.theme("GreenMono")
    layout = [
        [sg.Text("ファイルを選択して下さい", font=font, pad=[(15, 0), (15, 0)])],
        [sg.InputText(size=(21, 1), pad=[(15, 0), (0, 0)]), sg.FileBrowse(key="file")],
        [sg.Button("実行ファイル / 円グラフ", font=font, pad=((15, 10), (7, 0)))],
        [sg.Button("実行ファイル / 表", font=font, pad=((15, 10), (1, 0)))],
        [sg.Button("閲覧ページ / 円グラフ", font=font, pad=((15, 10), (1, 0)))],
        [sg.Button("閲覧ページ / 表", font=font, pad=((15, 10), (1, 10)))],
    ]
    return layout


def __create_file_compare():
    font = ("游明朝", 12)
    sg.theme("GreenMono")
    layout = [
        [sg.Text("ファイルを選択して下さい", font=font, pad=[(15, 0), (15, 0)])],
        [sg.Text("①", font=font, pad=[(15, 0), (0, 0)]), sg.InputText(size=(17, 1)), sg.FileBrowse(key="file1")],
        [sg.Text("②", font=font, pad=[(15, 0), (0, 0)]), sg.InputText(size=(17, 1)), sg.FileBrowse(key="file2")],
        [sg.Button("実行ファイル / 円グラフ", font=font, pad=((15, 10), (7, 0)))],
        [sg.Button("閲覧ページ / 円グラフ", font=font, pad=((15, 10), (1, 0)))],
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


if __name__ == "__main__":
    window = sg.Window('My window with tabs', create_layout())

    while True:
        event, values = window.read()
        print(event,values)
        if event == sg.WIN_CLOSED:
            break
