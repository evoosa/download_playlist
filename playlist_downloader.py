import os.path

from consts import PLAYLISTS, BASE_DIR, SPOTIFY_BASE_URL
import glob
from datetime import datetime
from utils import get_logger
from savify import Savify
from savify.types import Type, Format, Quality
from savify.utils import PathHolder
import dotenv

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
        self.logger.info(f"downloading playlist to {output_dir}")
        savify = Savify(api_credentials=(
            os.environ.get("SPOTIPY_CLIENT_ID"),
            os.environ.get("SPOTIPY_CLIENT_SECRET")),
            quality=Quality.BEST,
            download_format=Format.MP3,
            path_holder=PathHolder(downloads_path=output_dir),
            logger=get_logger(f"{output_dir}_{current_date}.log")
        )
        savify.download(playlist_url, query_type=Type.PLAYLIST)
        self.logger.info(f"done downloading playlist!")

    def _get_filenames(self, glob_pattern):
        filenames = []
        for filepath in glob.glob(glob_pattern):
            filenames.append(os.path.basename(filepath))
        self.logger.info(f"got {len(filenames)} that can be skipped")
        return filenames

    def _delete_empty_files(self, filenames, output_dir):
        for filename in filenames:
            file_to_del = os.path.join(output_dir, filename)
            if os.path.exists(file_to_del):
                os.remove(file_to_del)
        self.logger.info(f"deleted {len(filenames)} empty files")

    def _create_empty_files(self, filenames, output_dir):
        for filename in filenames:
            output_file_path = os.path.join(output_dir, filename)
            with open(output_file_path, 'w'):
                pass
        self.logger.info(f"created {len(filenames)} empty files")

    def backup_playlists_to_external_drive(self, drive_letter):
        """ backup the downloaded playlists to the given external drive """
        pass
