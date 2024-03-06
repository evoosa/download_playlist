from playlist_downloader import PlaylistDownloader
from utils import get_args

if __name__ == '__main__':
    args = get_args()
    playlist_key = args.playlist_key
    pd = PlaylistDownloader()

    if args.download_playlist:
        if not args.playlist_key:
            raise ValueError("GIB PLAYLIST KEY YA EFES")
        pd.download_playlist_diff(playlist_key)

    if args.sort_by_era:
        if not args.playlist_key:
            raise ValueError("GIB PLAYLIST KEY YA EFES")
        pd.sort_songs_by_era(playlist_key)

    if args.backup:
        if not (args.src_dir and args.dest_dir):
            raise ValueError("GIB SRC AND DEST DIR YA EFES")
        pd.backup_playlists(args.src_dir, args.dest_dir)
