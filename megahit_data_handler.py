import os
import json
import datetime
import matplotlib
from pprint import pprint
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange

def get_data():
    result = {}
    for file in os.listdir("data/radio3fm_megahit/"):
        json_data1 = open("data/radio3fm_megahit/"+file).read()
        spotify_data = json.loads(json_data1)
        print(str(file))
        for x in spotify_data:
            pprint(x['snippet']['title'])
    return result



# print(difference_likes_dislikes())

get_data()