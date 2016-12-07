import os
import json

folder = "youtube_top100"


for filename in os.listdir("data/"+folder):
    json_data2 = open("data/" + folder + "/" + str(filename)).read()
    youtube_data = json.loads(json_data2)
    indices = []
    for video in youtube_data:
        if "Jumpman" in video.get("snippet", {}).get("title", ""):
            indices.append(youtube_data.index(video))
        elif "Back to Back" in video.get("snippet", {}).get("title", ""):
            indices.append(youtube_data.index(video))
        elif "Big Rings" in video.get("snippet", {}).get("title", ""):
            indices.append(youtube_data.index(video))

    for i in indices:
        del youtube_data[i]

    with open("data/" + folder + "/" + str(filename), 'w') as outfile:
        json.dump(youtube_data, outfile)