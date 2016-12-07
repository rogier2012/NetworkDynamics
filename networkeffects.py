import os
import json
import datetime as dt
from datetime import datetime
from collections import defaultdict
from pprint import pprint

import matplotlib
import matplotlib.pyplot as plt
import numpy as np




def store_time_views():
    data = []
    for i in range(100):
        int_result = []
        result = {}
        song_name = ""
        for file in os.listdir("data/youtube_top100" + "/"):
            json_data1 = open("data/youtube_top100" + "/" + file).read()
            youtube = json.loads(json_data1)
            if (i < len(youtube)):
                entry = youtube[i]
            else:
                entry = {}
            year = int(file[:4])
            month = int(file[4:6])
            day = int(file[6:8])
            if (len(entry) > 0 and youtube.index(entry) != 73 and youtube.index(entry) != 22 and youtube.index(entry) != 67):
                if song_name == "": song_name = entry.get("snippet", {}).get("title", "")
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
                if (youtube.index(entry) == 73): print(entry)

        # for k,v in int_result:
        #     result[str(k)] = v
        if len(result) > 0: data.append(result)
    with open('data/intermediate_data/views_over_time.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

def plot_all_songs(derivative=False):
    json_data1 = open("data/intermediate_data/views_over_time.json").read()
    songs = json.loads(json_data1)
    json_data2 = open("data/youtube_top100/20160325_1800_data.json").read()
    youtube = json.loads(json_data2)
    for song in songs:
        data = dict_to_tuplelist(song,songs.index(song) == 73,date_conversion_needed=True)
        if (derivative):
            diff_data = derivative_data(data)
            plt.plot(*zip(*diff_data))
            x, y = (zip(*diff_data))
            x1 = np.array(range(len(x)))
            y1 = np.array(y)

            m, b = np.polyfit(x1, y1, 1)
            plt.plot(x, m * x1 + b, '-')



        else:
            plt.plot(*zip(*data))
        song_name=youtube[songs.index(song)].get("snippet", {}).get("title", "")
        plt.title(song_name)
        plt.savefig("figures/networkeffects/" + str(songs.index(song)) + song_name.split()[0]  + ".png")
        plt.close()


def plot_network_effects_songs():
    json_data1 = open("data/intermediate_data/views_over_time.json").read()
    songs = json.loads(json_data1)
    json_data2 = open("data/youtube_top100/20160325_1800_data.json").read()
    youtube = json.loads(json_data2)
    result = {'Yes':[], 'No':[]}
    for song in songs:
        data = dict_to_tuplelist(song, songs.index(song) == 73, date_conversion_needed=True)
        diff_data = derivative_data(data)
        x, y = (zip(*diff_data))
        x1 = np.array(range(len(x)))
        y1 = np.array(y)

        m, b = np.polyfit(x1, y1, 1)

        plt.plot(x, m * x1 + b, '-')
        plt.plot(*zip(*diff_data))

        song_name = youtube[songs.index(song)].get("snippet", {}).get("title", "")
        plt.title(song_name)
        plt.savefig("figures/networkeffects/" + str(songs.index(song)) + song_name.split()[0] + ".png")
        plt.close()
        if m < 0:
            result['Yes'].append(song_name)
        else:
            result['No'].append(song_name)
    return result


def derivative_data(input):
    result = []
    previous = 0
    for k,v in input:
        result.append((k,v-previous))
        previous = v

    del result[0]

    return result


def dict_to_tuplelist(input,drake,date_conversion_needed=False):
    result = []
    if drake: print(input)
    for k,v in input.items():
        if (date_conversion_needed):
            d = datetime.strptime(k,"%Y-%m-%d")
            result.append((d,v))
        else:
            result.append((k,v))

    return sorted(result)


def dsum(*dicts):
    ret = defaultdict(int)
    for d in dicts:
        for k, v in d.items():
            ret[k] += v
    return dict(ret)

def get_all_data_derivative():
    with open('data/intermediate_data/'+'views_over_time'+'.json') as data_file:
        print('lol')
        average_views = {}
        data = json.load(data_file)
        first_entry = data.pop(0)
        for key, value in first_entry.items():
            average_views[key] = value
        for entry in data:
            average_views = dsum(average_views,entry )
        for key, value in average_views.items():
            average_views[key] = value//98
        average_views_tuple = dict_to_tuplelist(average_views, True)
        diff_data = []
        index_diff_data = []
        counter = 1
        previous = 0
        for k, v in average_views_tuple:
            diff_data.append((k, v - previous))
            index_diff_data.append((counter, v - previous))
            previous = v
            counter = counter+1
        del diff_data[0]
        del index_diff_data[0]
        x, y = (zip(*index_diff_data))
        x = np.array(x)
        y = np.array(y)
        m, b = np.polyfit(x, y, 1)
        # plt.plot(x, m * x + b, '-')
        plt.title('total')
        # plt.plot(*zip(*index_diff_data))
        plt.plot(*zip(*average_views_tuple))
        print(diff_data)
        print(index_diff_data)
        plt.show()


# get_all_data_derivative()

def str_to_date(strs):
    result=[]
    for item in strs:
        result.append(datetime.strptime(item,"%Y-%m-%d"))
    return result



# plot_all_songs(derivative=True)
print(plot_network_effects_songs())

