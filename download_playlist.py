#!/usr/bin/env python3

import csv
import os
import sys

GENRE = "FIXME"
playlist_name = "FIXME"
# playlist_name = sys.argv[1]

csv_path = fr".\csvs\{playlist_name}.csv"
output_dir = fr".\output_dirs\{playlist_name}"

# create output dir if missing
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# open up the csv file and read the data into a list
with open(csv_path, 'r', newline="", encoding='utf-8', errors='ignore') as f:
    print(f"READING CSV: {csv_path}")
    reader = csv.reader(f)
    data = list(reader)

# skip the first line which contains headings
for item in data[1:]:
    try:
        # create a song name to search for using the artist and song title
        search = item[3] + " " + item[1]
        filename = f"{item[3]} - {item[1]}"
        print(f"DOWNLOADING: {filename}")

        untagged_mp3_path = f"{output_dir}/{filename}.untagged.mp3"
        untagged_wav_path = f"{output_dir}/{filename}.untagged.wav"
        mp3_path = f"{output_dir}/{filename}.mp3"

        if not os.path.exists(mp3_path):
            # download the audio as a temporary mp3 file
            print(f"DOWNLOADING MP3: {untagged_mp3_path}")
            ydl_cmd = f'yt-dlp.exe "ytsearch1:{search}" -f ba --max-filesize 100m --extract-audio --audio-format mp3 -o "{untagged_mp3_path}"'
            os.system(ydl_cmd)

            # if file is a wav, convert it to mp3
            if os.path.exists(untagged_wav_path):
                print(f"CONVERTING TO MP3: {untagged_mp3_path}")
                convert_to_mp3_cmd = f"ffmpeg -i {untagged_wav_path} -codec:a libmp3lame -qscale:a 2 {untagged_wav_path}"
                os.system(convert_to_mp3_cmd)
                os.remove(untagged_wav_path)

            # copy and tag the file
            print(f"TAGGING: {mp3_path}")
            ffmpeg_cmd = f'ffmpeg -i "{untagged_mp3_path}" -id3v2_version 3 -metadata artist="{item[3]}" -metadata album="{item[5]}" -metadata album_artist="{item[7]}" -metadata title="{item[1]}" -metadata genre="{GENRE}" -metadata date="{item[8][:4]}" -hide_banner -loglevel error "{mp3_path}" -y'
            os.system(ffmpeg_cmd)

            # delete the temp file
            os.remove(untagged_mp3_path)
        else:
            print(f"FILE {mp3_path} EXISTS, SKIPPING...")

    except Exception as e:
        print(f"ERROR: {e}")
