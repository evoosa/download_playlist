import os.path
import shutil

from consts import PLAYLISTS, BASE_DIR, SPOTIFY_BASE_URL, ERAS, DATA_DIR
import glob
from datetime import datetime
from utils import get_logger, unwindows, create_dir_if_missing
from savify import Savify
from savify.types import Type, Format, Quality
from savify.utils import PathHolder
import dotenv
from mutagen.easyid3 import EasyID3

current_date = datetime.now().strftime('%d_%m_%Y')
dotenv.load_dotenv()


class PlaylistDownloader:
    def __init__(self):
        # create the base output directory
        self.base_output_dir = os.path.join(BASE_DIR, f"new_music_{current_date}")
        self.logger = get_logger(f"{self.base_output_dir}.log")
        self.logger.debug("created logger")

        if not os.path.exists(self.base_output_dir):
            os.makedirs(self.base_output_dir)
            self.logger.info(f"created base dir: {self.base_output_dir}")
        pass

    def download_playlist_diff(self, playlist_key):
        """ download new songs added to the given playlist """
        # create output dir
        output_dir = os.path.join(self.base_output_dir, playlist_key)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            self.logger.info(f"created base dir: {output_dir}")

        # create empty files, so savify won't re-download them
        filenames = self._get_filenames(os.path.join(BASE_DIR, PLAYLISTS[playlist_key]['search_pattern']))
        self._create_empty_files(filenames, output_dir)

        # download the newly added tracks
        self._download_playlist(output_dir, f"{SPOTIFY_BASE_URL}{PLAYLISTS[playlist_key]['playlist_id']}")
        self.logger.info(f"done downloading playlist {playlist_key} to {output_dir}")

        # delete empty files
        self._delete_empty_files(filenames, output_dir)

    def _download_playlist(self, output_dir, playlist_url):
        """ download a playlist using savify """
        self.logger.info(f"downloading playlist to {output_dir}")
        savify = Savify(api_credentials=(
            os.environ.get("SPOTIPY_CLIENT_ID"),
            os.environ.get("SPOTIPY_CLIENT_SECRET")),
            quality=Quality.BEST,
            download_format=Format.MP3,
            path_holder=PathHolder(
                downloads_path=output_dir,
                data_path=os.path.join(output_dir, DATA_DIR)
            ),

            logger=get_logger(f"{output_dir}_{current_date}.log")
        )
        savify.download(playlist_url, query_type=Type.PLAYLIST)
        self.logger.info(f"done downloading playlist!")

    def _get_filenames(self, glob_pattern):
        """ get all filenames under the supplied glob search pattern """
        filenames = []
        for filepath in glob.glob(glob_pattern):
            filenames.append(os.path.basename(filepath))
        self.logger.info(f"got {len(filenames)} that can be skipped")
        return filenames

    def _delete_empty_files(self, filenames, output_dir):
        """ delete the empty files we created to prevent duplicate downloads """
        for filename in filenames:
            file_to_del = os.path.join(output_dir, filename)
            if os.path.exists(file_to_del):
                os.remove(file_to_del)
        self.logger.info(f"deleted {len(filenames)} empty files")

    def _create_empty_files(self, filenames, output_dir):
        """ create empty files so savify won't re-download them """
        for filename in filenames:
            output_file_path = os.path.join(output_dir, filename)
            with open(output_file_path, 'w'):
                pass
        self.logger.info(f"created {len(filenames)} empty files")

    def backup_playlists(self, src_path, dest_path):
        """ backup the downloaded playlists to the given destination (can be an external drive) """

        def backup_track(track_name: str, src_dir: str, dest_dir: str):
            """ backup tracks to dest dir if they don't exist """
            dest_track_path = unwindows(os.path.join(dest_dir, track_name))
            if os.path.exists(dest_track_path):
                self.logger.debug(f"track {dest_track_path} exists in dest, not copying..")
            else:
                shutil.copy(unwindows(os.path.join(src_dir, track_name)), dest_track_path)
                self.logger.info(f"copied track to {dest_track_path}")

        create_dir_if_missing(dest_path)
        for p in os.listdir(src_path):
            if p != DATA_DIR:
                path = unwindows(os.path.join(src_path, p))
                # if we're in a subdirectory, backup it's contents
                if os.path.isdir(path):
                    self.logger.debug(f"{p} is subdir, diving in..")
                    dest_subdir = unwindows(os.path.join(dest_path, p))
                    create_dir_if_missing(dest_subdir)
                    for track in os.listdir(path):
                        backup_track(track, path, dest_subdir)
                # if it's a file, back it up
                else:
                    backup_track(p, src_path, dest_path)

    def sort_songs_by_era(self, playlist_key):
        """ sort the songs in the given directory by era, output to a subdirectory """
        output_dir = os.path.join(self.base_output_dir, playlist_key)
        self.logger.info(f"sorting: {output_dir}")
        for track_path in glob.glob(f"{output_dir}/*"):
            try:
                release_year = (EasyID3(track_path)['date'][0][:4])
                for era in ERAS.keys():
                    if int(release_year) in ERAS[era]:
                        era_subdir = os.path.join(output_dir, era)
                        if not os.path.exists(era_subdir):
                            os.makedirs(era_subdir)
                            self.logger.info(f"created era subdir: {era_subdir}")
                        shutil.move(track_path, era_subdir)
                        self.logger.debug(f"moved {track_path} to era subdir: {era}")
            except Exception as e:
                self.logger.error(f"pasten... {e}")
