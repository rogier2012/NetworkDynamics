import json

json_data1=open("data/spotify_top100/20151109_1800_data.json").read()
spotify_data = json.loads(json_data1)
json_data2=open("data/youtube_top100/20161128_1800_data.json").read()
youtube_data = json.loads(json_data2)
print(len(youtube_data))
# print(youtube_data[0].get("snippet",{}).get("title"),"")
spotify_tracks = spotify_data.get("tracks").get("items", [])
for track in spotify_tracks:
    track_name = track.get("track",{}).get("name","")
    video_name = youtube_data[spotify_tracks.index(track)].get("snippet",[]).get("title","")
    statistics = youtube_data[spotify_tracks.index(track)].get("statistics",{})
    likes = statistics.get("likeCount")
    dislikes = statistics.get("dislikeCount")
    # print(track_name + " with " + str(likes) + " likes and "  + str(dislikes) + " dislikes")

    print(track_name + " youtube: " + video_name + " index " + str(spotify_tracks.index(track)))