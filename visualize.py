import csv
import datetime
import matplotlib.pyplot as plt
# import numpy as np


def show_result(filename, data_mode, chart_mode, win_name="result"):
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
        make_pie_chart(data, win_name)
    elif chart_mode == "table":
        make_table(data, win_name)


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
        if "timane" in l[i][2] or l[i][1] == "":
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


def make_pie_chart(d, win_name):
    labels = list(d.keys())
    sizes = list(d.values())
    max_label_len = max([len(label) for label in labels])
    if max_label_len > 70:
        max_label_len = 70
        labels = [label[:70] + "..." if len(label) > 70 else label for label in labels]

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
    plt.figure(win_name, figsize=(fig_width, 5))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", counterclock=False, startangle=90, labeldistance=None, center=(0, 0))
    plt.axis("equal")
    plt.xlim(*xrange)
    plt.legend(bbox_to_anchor=(legend_x, 0.85), loc="upper left", borderaxespad=0, fontsize=14)
    if win_name == "result":
        plt.show()


def make_table(d, win_name):
    labels = list(d.keys())
    sizes = list(d.values())
    for i in range(len(sizes)):
        sizes[i] = str(datetime.timedelta(seconds=sizes[i]))
    max_label_len = max([len(label) for label in labels])
    if max_label_len > 70:
        max_label_len = 70
        labels = [label[:70] + "..." if len(label) > 70 else label for label in labels]

    width = (max_label_len + 10) * 0.186
    height = (len(labels) + 3) * 0.5
    plt.figure(win_name, figsize=(width, height))
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
    if win_name == "result":
        plt.show()


# def show_time_flow(filename):
#     if filename == "":
#         return
#     data = read_csv(filename)
#     data = calc_time_diff(data)
#     print(data)
#     # data = calc_exe_time(data)
#     labels = [row[2] for row in data]
#     sizes = [int(row[0]) for row in data]
#     normalized = (np.array(sizes) / sum(sizes)).reshape(1, -1)
#     N, K = 1, len(labels)
#     tick_labels = ["a"]

#     print(normalized.shape)
#     cumulative = 0
#     tick = [0]

#     for k in range(K):
#         color = plt.cm.viridis(float(k) / K, 1)
#         plt.barh(tick, normalized[:, k], left=cumulative, color=color, label=labels[k])
#         cumulative += normalized[:, k]

#     plt.xlim((0, 1))
#     plt.yticks(tick, tick_labels)
#     plt.legend()
#     plt.show()


if __name__ == "__main__":
    raw = read_csv("timane/test.csv")
    # show_time_flow("timane_csvdata/20220916.csv")
