import os.path

from consts import PLAYLISTS, BASE_DIR, SPOTIFY_BASE_URL
import glob
from datetime import datetime
from utils import get_logger

current_date = datetime.now()


class PlaylistDownloader:
    def __init__(self):
        # create the base output directory
        self.base_output_dir = os.path.join(BASE_DIR, f"new_music_{current_date.strftime('%d_%m_%Y')}")
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

    def _get_filenames(self, glob_pattern):
        filenames = []
        for filepath in glob.glob(glob_pattern):
            filenames.append(os.path.basename(filepath))
        self.logger.info(f"got {len(filenames)} that can be skipped")
        return filenames

    def _create_empty_files(self, filenames, output_dir):
        for filename in filenames:
            output_file_path = os.path.join(output_dir, filename)
            with open(output_file_path, 'w'):
                pass
        self.logger.info(f"created {len(filenames)} empty files")

    def backup_playlists_to_external_drive(self, drive_letter):
        """ backup the downloaded playlists to the given external drive """
        pass
