import logging
from os.path import join as pathjoin
from os.path import dirname
module_path = dirname(__file__)
imgroot = pathjoin(module_path, 'imgs')

def setup_logger(name, loglevel = logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(loglevel)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(loglevel)
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger

from general import *