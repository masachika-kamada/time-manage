import csv
import datetime
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def show_result(filename, data_mode, chart_mode):
    data = read_csv(filename)
    data = calc_time_diff(data)
    if data_mode == "exe":
        data = calc_exe_time(data)
    elif data_mode == "page":
        data = calc_page_time(data)
    data = sort_and_cut(data, 10)
    if chart_mode == "pie":
        make_pie_chart(data)
    elif chart_mode == "bar":
        make_bar_chart(data)


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
    plt.figure(figsize=(10, 5))
    labels = list(d.keys())
    sizes = list(d.values())
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", counterclock=False, startangle=90, labeldistance=None, center=(2.65, 0))
    plt.axis("equal")
    plt.xlim(0, 8)
    plt.legend(bbox_to_anchor=(0.5, 0.85), loc="upper left", borderaxespad=0, fontsize=14)
    plt.show()


def make_bar_chart(d):
    labels = list(d.keys())
    sizes = list(d.values())
    sns.barplot(x=sizes, y=labels, orient="h", palette="Blues_d", linewidth=0.5, edgecolor="black", saturation=0.5, ci=None, errcolor="black", errwidth=1)
    plt.show()


if __name__ == "__main__":
    raw = read_csv("timane/20220909.csv")
    pprint(raw)
    l = calc_time_diff(raw)
    pprint(l)

    exe_time = calc_exe_time(l)
    exe_time = sort_and_cut(exe_time, 10)
    pprint(exe_time)
    make_pie_chart(exe_time)
    make_bar_chart(exe_time)

    page_time = calc_page_time(l)
    page_time = sort_and_cut(page_time, 10)
    pprint(page_time)
    make_pie_chart(page_time)
    make_bar_chart(page_time)
