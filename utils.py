import logging


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
