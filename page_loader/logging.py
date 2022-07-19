import logging


def init_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()
    FORMAT_CONSOLE = '%(levelname)s : %(name)s : %(message)s'
    sh.setFormatter(logging.Formatter(FORMAT_CONSOLE))
    sh.setLevel(logging.INFO)

    fh = logging.FileHandler(filename='./logger.log')
    FORMAT = '%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s'
    fh.setFormatter(logging.Formatter(FORMAT))
    fh.setLevel(logging.DEBUG)

    logger.addHandler(sh)
    logger.addHandler(fh)
