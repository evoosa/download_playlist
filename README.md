# Download Spotify/Youtube Playlist from CSV

## example:

1. download the playlist's CSV from:
    * Exportify (spotify playlists)
    * https://www.tunemymusic.com/transfer/youtube-to-file (youtube playlists)

2. open it in google sheets and save to convert to utf-8
    * arrange it: [1]track, [3]artist, [5]album

3. fix: "playlist_name", "GENRE"

4. download the tracks by running:
   ```
   ./download_playlist.py
   ```