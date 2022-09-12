import csv
import datetime
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def show_result(filename, data_mode, chart_mode):
    if filename == "":
        return
    data = read_csv(filename)
    data = calc_time_diff(data)
    if data_mode == "exe":
        data = calc_exe_time(data)
    elif data_mode == "page":
        data = calc_page_time(data)
    data = sort_and_cut(data, 10)
    if chart_mode == "pie":
        make_pie_chart(data)
    elif chart_mode == "table":
        make_table(data)


def read_csv(filename):
    with open(filename, "r", encoding="shift-jis", errors="ignore") as f:
        reader = csv.reader(f)
        return [row for row in reader]


def calc_time_diff(l):
    prev = ""
    timane_idx = []
    for i in reversed(range(0, len(l))):
        t = datetime.datetime.strptime(l[i][0], "%Y/%m/%d %H:%M:%S")
        if prev == "":
            prev = t
            continue
        l[i][0] = int((prev - t).total_seconds())
        prev = t
        if l[i][1] == "タイマネ":
            timane_idx.append(i)
    for i in timane_idx:
        l.pop(i)
    return l[:-1]


def calc_exe_time(l):
    d = {}
    for i in range(0, len(l)):
        if l[i][2] in d:
            d[l[i][2]] += l[i][0]
        else:
            d[l[i][2]] = l[i][0]
    return d


def calc_page_time(l):
    d = {}
    for i in range(0, len(l)):
        if l[i][1] in d:
            d[l[i][1]] += l[i][0]
        else:
            d[l[i][1]] = l[i][0]
    return d


def sort_and_cut(d, n):
    return dict(sorted(d.items(), key=lambda x: x[1], reverse=True)[:n])


def make_pie_chart(d):
    labels = list(d.keys())
    sizes = list(d.values())
    max_label_len = max([len(label) for label in labels])
    print(max_label_len)
    if max_label_len <= 10:
        fig_width = 7
        xrange = (-1, 2.3)
        legend_x = 0.7
    elif max_label_len <= 20:
        fig_width = 9
        xrange = (-1, 3.7)
        legend_x = 0.48
    elif max_label_len <= 30:
        fig_width = 10.7
        xrange = (-1, 4.6)
        legend_x = 0.38
    elif max_label_len <= 40:
        fig_width = 12.4
        xrange = (-1, 5.8)
        legend_x = 0.29
    elif max_label_len <= 50:
        fig_width = 14
        xrange = (-1, 6.8)
        legend_x = 0.22
    else:
        fig_width = 16
        xrange = (-1, 7.8)
        legend_x = 0.2
    plt.figure(figsize=(fig_width, 5))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", counterclock=False, startangle=90, labeldistance=None, center=(0, 0))
    plt.axis("equal")
    plt.xlim(*xrange)
    plt.legend(bbox_to_anchor=(legend_x, 0.85), loc="upper left", borderaxespad=0, fontsize=14)
    plt.show()


# def make_bar_chart(d):
#     labels = list(d.keys())
#     sizes = list(d.values())
#     sns.barplot(x=sizes, y=labels, orient="h", palette="Blues_d", linewidth=0.5, edgecolor="black", saturation=0.5, ci=None, errcolor="black", errwidth=1)
#     plt.show()


def make_table(d):
    labels = list(d.keys())
    sizes = list(d.values())
    for i in range(len(sizes)):
        sizes[i] = str(datetime.timedelta(seconds=sizes[i]))
    max_label_len = max([len(label) for label in labels])

    width = (max_label_len + 10) * 0.186
    height = (len(labels) + 3) * 0.5
    plt.figure(figsize=(width, height))
    plt.axis("off")
    plt.axis("tight")

    table = plt.table(cellText=list(zip(labels, sizes)),
                      colLabels=["ページ名", "時間"],
                      loc="center",
                      colWidths=[max_label_len + 4, 9],
                      bbox=[0, 0, 1, 1])

    table[0, 0].set_facecolor("#363636")
    table[0, 1].set_facecolor("#363636")
    table[0, 0].set_text_props(color="w")
    table[0, 1].set_text_props(color="w")
    table.auto_set_font_size(False)
    table.set_fontsize(13)
    plt.show()


if __name__ == "__main__":
    raw = read_csv("timane/test.csv")
    pprint(raw)
    l = calc_time_diff(raw)
    pprint(l)

    exe_time = calc_exe_time(l)
    exe_time = sort_and_cut(exe_time, 10)
    pprint(exe_time)
    make_pie_chart(exe_time)
    # make_table(exe_time)

    # page_time = calc_page_time(l)
    # page_time = sort_and_cut(page_time, 10)
    # pprint(page_time)
    # make_pie_chart(page_time)
    # make_table(page_time)
