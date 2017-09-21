import logging
import os

PATH_TO_LOGGER_FILE = os.path.dirname(os.path.abspath(__file__)) + "/main_logs.log"
logging.basicConfig(level=logging.INFO, filename=PATH_TO_LOGGER_FILE, filemode="w")
LOGGER = logging.getLogger()
