import sys

from playlist_downloader import PlaylistDownloader
from utils import get_args

if __name__ == '__main__':
    args = get_args()
    playlist_key = args.playlist_key
    pd = PlaylistDownloader()
    if args.download_playlist:
        pd.download_playlist_diff(playlist_key)

    if args.sort_by_era:
        pd.sort_songs_by_era(playlist_key)
