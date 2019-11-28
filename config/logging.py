import logging


def config_log():
    # logging config
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
    # fp = logging.FileHandler('log.txt', encoding='utf-8')
    fs = logging.StreamHandler()
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT,
                        datefmt=DATE_FORMAT, handlers=[fs])
