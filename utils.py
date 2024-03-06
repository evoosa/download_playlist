import logging
import argparse
import os


def unwindows(string):
    return string.replace("\\", "/")


def create_dir_if_missing(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sort-by-era', action='store_true', help='sort the playlist tracks by era')
    parser.add_argument('-k', '--playlist-key', type=str, required=False, help='the playlist\'s key')
    parser.add_argument('-d', '--download-playlist', action='store_true', help='download the playlist')
    parser.add_argument('-b', '--backup', action='store_true', help='backup the given src dir to dest dir')
    parser.add_argument('--src-dir', type=str, required=False, help='source dir to backup')
    parser.add_argument('--dest-dir', type=str, required=False, help='dest dir to backup to')

    return parser.parse_args()


def get_logger(log_file_path):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create a formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # file handler
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)

    # add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
