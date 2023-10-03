# -*- coding: utf-8 -*-
import csv

from utils import *

data_list = get_datatable_files()
music_attribute_data = data_list[0]
music_order_data = data_list[1]
musicinfo_data = data_list[2]
wordlist_data = data_list[3]

musicinfo_based_list = []

for musicinfo in musicinfo_data:
    music = {
        "uniqueId": musicinfo["uniqueId"],
        "songId": musicinfo["id"],
        "songName": "",
        "songSubName": "",
        "musicinfo_genreNo": musicinfo["genreNo"],
        "music_order_genreNo": [],
        "starEasy": musicinfo["starEasy"],
        "starNormal": musicinfo["starNormal"],
        "starHard": musicinfo["starHard"],
        "starMania": musicinfo["starMania"],
        "starUra": musicinfo["starUra"],
        "new": "NO"
    }
    musicinfo_based_list.append(music)

for music_order in music_order_data:
    unique_id = music_order["uniqueId"]
    for music in musicinfo_based_list:
        if music["uniqueId"] == unique_id:
            genreNo = music["music_order_genreNo"]
            if music_order["genreNo"] not in genreNo:
                genreNo.append(music_order["genreNo"])
            break

for wordlist in wordlist_data:
    key = wordlist["key"]
    if key.startswith("song_sub_"):
        song_id = key.split("song_sub_")[1]
        for music in musicinfo_based_list:
            if music["songId"] == song_id:
                music["songSubName"] = wordlist["japaneseText"]
                break
    elif key.startswith("song_detail_"):
        continue
    elif key.startswith("song_"):
        song_id = key.split("song_")[1]
        for music in musicinfo_based_list:
            if music["songId"] == song_id:
                music["songName"] = wordlist["japaneseText"]
                break
    else:
        continue

for music_attribute in music_attribute_data:
    unique_id = music_attribute["uniqueId"]
    for music in musicinfo_based_list:
        if music["uniqueId"] == unique_id:
            if music_attribute["new"]:
                music["new"] = "YES"
            else:
                music["new"] = "NO"
            break

musicinfo_based_list = sorted(musicinfo_based_list, key=lambda k: k["uniqueId"])

headers = ["uniqueId", "songId", "songName", "songSubName", "musicinfo_genreNo", "music_order_genreNo",
           "starEasy", "starNormal", "starHard", "starMania", "starUra", "new"]

f_csv = open(output_musicinfo_table_filepath, "w+", encoding='utf-8-sig', newline="")
writer = csv.writer(f_csv)
writer.writerow(headers)

for music in musicinfo_based_list:
    writer.writerow([music["uniqueId"], music["songId"], music["songName"], music["songSubName"],
                     music["musicinfo_genreNo"], music["music_order_genreNo"], music["starEasy"], music["starNormal"],
                     music["starHard"], music["starMania"], music["starUra"], music["new"]])

f_csv.close()

music_order_based_list = []
for music_order in music_order_data:
    music = {
        "music_order_genreNo": music_order["genreNo"],
        "uniqueId": music_order["uniqueId"],
        "songId": music_order["id"],
        "songName": "",
        "songSubName": "",
        "musicinfo_genreNo": "",
        "starEasy": "",
        "starNormal": "",
        "starHard": "",
        "starMania": "",
        "starUra": "",
        "new": "NO",
    }
    music_order_based_list.append(music)

for wordlist in wordlist_data:
    key = wordlist["key"]
    if key.startswith("song_sub_"):
        song_id = key.split("song_sub_")[1]
        for music in music_order_based_list:
            if music["songId"] == song_id:
                music["songSubName"] = wordlist["japaneseText"]
    elif key.startswith("song_detail_"):
        continue
    elif key.startswith("song_"):
        song_id = key.split("song_")[1]
        for music in music_order_based_list:
            if music["songId"] == song_id:
                music["songName"] = wordlist["japaneseText"]
    else:
        continue

for music_attribute in music_attribute_data:
    unique_id = music_attribute["uniqueId"]
    for music in music_order_based_list:
        if music["uniqueId"] == unique_id:
            if music_attribute["new"]:
                music["new"] = "YES"
            else:
                music["new"] = "NO"

for musicinfo in musicinfo_data:
    unique_id = musicinfo["uniqueId"]
    for music in music_order_based_list:
        if music["uniqueId"] == unique_id:
            music["musicinfo_genreNo"] = musicinfo["genreNo"]
            music["starEasy"] = musicinfo["starEasy"]
            music["starNormal"] = musicinfo["starNormal"]
            music["starHard"] = musicinfo["starHard"]
            music["starMania"] = musicinfo["starMania"]
            music["starUra"] = musicinfo["starUra"]

headers = ["music_order_genreNo", "uniqueId", "songId", "songName", "songSubName", "musicinfo_genreNo",
           "starEasy", "starNormal", "starHard", "starMania", "starUra", "new"]

f_csv = open(output_music_order_table_filepath, "w+", encoding='utf-8-sig', newline="")
writer = csv.writer(f_csv)
writer.writerow(headers)

for music in music_order_based_list:
    writer.writerow([music["music_order_genreNo"], music["uniqueId"], music["songId"], music["songName"],
                     music["songSubName"], music["musicinfo_genreNo"], music["starEasy"], music["starNormal"],
                     music["starHard"], music["starMania"], music["starUra"], music["new"]])

f_csv.close()

print("Done!\nOutput files: " + output_musicinfo_table_filepath + ", " + output_music_order_table_filepath + "\n")
