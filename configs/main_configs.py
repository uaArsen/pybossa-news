import logging
import os

"""
Main configs.
"""
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH_TO_LOGGER_FILE = os.path.join(BASE_DIR, "main_logs.log")
logging.basicConfig(level=logging.INFO, filename=PATH_TO_LOGGER_FILE, filemode="w")
LOGGER = logging.getLogger()
