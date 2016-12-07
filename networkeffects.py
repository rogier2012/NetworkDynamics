import os
import json
import datetime as dt
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import random


def store_time_views():
    data = []
    for i in range(100):
        int_result = []
        result = {}
        song_name = ""
        for file in os.listdir("data/youtube_top95" + "/"):
            json_data1 = open("data/youtube_top95" + "/" + file).read()
            youtube = json.loads(json_data1)
            if i < len(youtube):
                entry = youtube[i]
            else:
                entry = {}
            year = int(file[:4])
            month = int(file[4:6])
            day = int(file[6:8])
            if len(entry) > 0 :
                if song_name == "":
                    song_name = entry.get("snippet", {}).get("title", "")
                if str(file) == "20160530_1800_data.json":
                    (key, viewCount) = int_result[len(int_result) - 1]
                    step = (int(entry['statistics']['viewCount']) - viewCount) // 4
                    d27 = dt.date(2016, 5, 27)
                    d28 = dt.date(2016, 5, 28)
                    d29 = dt.date(2016, 5, 29)
                    int_result.append((d27, viewCount + step))
                    int_result.append((d28, viewCount + 2 * step))
                    int_result.append((d29, viewCount + 3 * step))
                    result[str(d27)] = viewCount + step
                    result[str(d28)] = viewCount + 2 * step
                    result[str(d29)] = viewCount + 3 * step

                elif str(file) == "20160808_1800_data.json":
                    (key, viewCount) = int_result[len(int_result) - 1]
                    step = (int(entry['statistics']['viewCount']) - viewCount) // 3
                    d06 = dt.date(2016, 8, 6)
                    d07 = dt.date(2016, 8, 7)
                    int_result.append((d06, viewCount + step))
                    int_result.append((d07, viewCount + 2 * step))
                    result[str(d06)] = viewCount + step
                    result[str(d07)] = viewCount + 2 * step

                int_result.append((dt.date(year, month, day), int(entry['statistics']['viewCount'])))
                result[str(dt.date(year, month, day))] = int(entry['statistics']['viewCount'])


        if len(result) > 0:
            data.append(result)
    with open('data/intermediate_data/views_over_time.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)


def plot_all_songs(derivative=False):
    json_data1 = open("data/intermediate_data/views_over_time.json").read()
    songs = json.loads(json_data1)
    json_data2 = open("data/youtube_top95/20160325_1800_data.json").read()
    youtube = json.loads(json_data2)
    for song in songs:
        data = dict_to_tuple_list(song, date_conversion_needed=True)
        suffix = ""
        if derivative:
            diff_data = derivative_data(data)
            plt.plot(*zip(*diff_data))
            x, y = (zip(*diff_data))
            x1 = np.array(range(len(x)))
            y1 = np.array(y)

            m, b = np.polyfit(x1, y1, 1)
            plt.plot(x, m * x1 + b, '-')
            suffix = "_diff"
        else:
            plt.plot(*zip(*data))
        song_name = youtube[songs.index(song)].get("snippet", {}).get("title", "")
        plt.title(song_name)
        plt.savefig("figures/networkeffects/" + str(songs.index(song)) + song_name.split()[0] + suffix + ".png")
        plt.close()


def plot_network_effects_songs(index=False):
    json_data1 = open("data/intermediate_data/views_over_time.json").read()
    songs = json.loads(json_data1)
    json_data2 = open("data/youtube_top95/20160325_1800_data.json").read()
    youtube = json.loads(json_data2)
    result = {True: [], False: []}
    for song in songs:
        data = dict_to_tuple_list(song, date_conversion_needed=True)
        diff_data = derivative_data(data)
        x, y = (zip(*diff_data))
        x1 = np.array(range(len(x)))
        y1 = np.array(y)

        m, b = np.polyfit(x1, y1, 1)

        # plt.plot(x, m * x1 + b, '-')
        # plt.plot(*zip(*diff_data))

        song_name = youtube[songs.index(song)].get("snippet", {}).get("title", "")
        filename = str(songs.index(song)) + song_name.split()[0] + "_diff"
        # plt.title(song_name)
        # plt.savefig("figures/networkeffects/" + filename + ".png")
        # plt.close()
        if index:

            result[(m < 0)].append(filename + ".png")
        else:

            result[(m < 0)].append(song_name)
    return result


def derivative_data(input_dict):
    result = []
    previous = 0
    for k, v in input_dict:
        result.append((k, v - previous))
        previous = v

    del result[0]

    return result


def dict_to_tuple_list(input_dict, date_conversion_needed=False):
    result = []
    for k, v in input_dict.items():
        if date_conversion_needed:
            d = datetime.strptime(k, "%Y-%m-%d")
            result.append((d, v))
        else:
            result.append((k, v))

    return sorted(result)


# get_all_data_derivative()

def str_to_date(strs):
    result = []
    for item in strs:
        result.append(datetime.strptime(item, "%Y-%m-%d"))
    return result


def five_random_songs():
    data = plot_network_effects_songs(index=True)
    plots = {True: [], False: []}
    for k in data:
        for i in range(5):
            r = random.choice(data[k])
            while r in plots[k]:
                r = random.choice(data[k])
            plots[k].append(r)

    for k in plots:
        print("\\begin{figure}")
        for c in plots[k]:
            print("\\includegraphics[width=0.33\\textwidth]{figures/networkeffects/" + c + "}")
        print("\\end{end}")


five_random_songs()
def size_network_effect_sets():
    data1 = plot_network_effects_songs()
    for bool1 in data1:
        print(str(bool1) + ": " + str(len(data1[bool1])))

# size_network_effect_sets()
# plot_all_songs(derivative=True)
# store_time_views()