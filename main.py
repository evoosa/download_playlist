import sys

from playlist_downloader import PlaylistDownloader

if __name__ == '__main__':
    playlist_key = sys.argv[1]
    pd = PlaylistDownloader()
    pd.download_playlist_diff(playlist_key)
