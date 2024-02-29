import logging
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sort-by-era', action='store_true', help='sort the playlist tracks by era')
    parser.add_argument('-k', '--playlist-key', type=str, help='the playlist\'s key')
    parser.add_argument('-d', '--download-playlist', action='store_true', help='download the playlist')
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
