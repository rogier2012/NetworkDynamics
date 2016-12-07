import json
import os
# json_data1=open("data/spotify_top100/20151109_1800_data.json").read()
# spotify_data = json.loads(json_data1)
# json_data2=open("data/youtube_top100/20161128_1800_data.json").read()
# youtube_data = json.loads(json_data2)
# print(len(youtube_data))
# # print(youtube_data[0].get("snippet",{}).get("title"),"")
# spotify_tracks = spotify_data.get("tracks").get("items", [])
# for track in spotify_tracks:
#     track_name = track.get("track",{}).get("name","")
#     video_name = youtube_data[spotify_tracks.index(track)].get("snippet",[]).get("title","")
#     statistics = youtube_data[spotify_tracks.index(track)].get("statistics",{})
#     likes = statistics.get("likeCount")
#     dislikes = statistics.get("dislikeCount")
#     # print(track_name + " with " + str(likes) + " likes and "  + str(dislikes) + " dislikes")
#
#     print(track_name + " youtube: " + video_name + " index " + str(spotify_tracks.index(track)))
counter = 0
folder = "youtube_top100"


for filename in os.listdir("data/"+folder):
    counter += 1
    json_data2 = open("data/"+folder+"/"+str(filename)).read()
    youtube_data = json.loads(json_data2)
    print(str(counter) + ". " + filename)
    print(len(youtube_data))

    break

# for filename in os.listdir("figures/cascades"):
#     print("\\includegraphics[width=0.5\\textwidth]{figures/cascades/" + filename + "}")
