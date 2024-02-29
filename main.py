import os

from playlist_downloader import PlaylistDownloader

if __name__ == '__main__':
    pd = PlaylistDownloader()
    pd.download_playlist_diff("all_time_favs")