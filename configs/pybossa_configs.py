import main_configs
import os

"""
Pybossa related configs.
"""
ENDPOINT = os.environ.get('PYBOSSA_ENDPOINT', 'http://ec2-18-194-103-85.eu-central-1.compute.amazonaws.com:5000')
API_KEY = os.environ.get('PYBOSSA_KEY', 'fd45bdd1-e2e3-45d0-80d4-f17969d61d4f')
PROJECT_CONFIGS = os.environ.get('PYBOSSA_PROJECT',
                                 os.path.join(main_configs.BASE_DIR, "pybossa_importer", "project.json"))
TASKS = os.environ.get('PYBOSSA_TASKS', os.path.join(main_configs.BASE_DIR, "tmp", "reuters.json"))
REDUNDANCY = os.environ.get('PYBOSSA_REDUNDANCY', 3)
OUTPUT = os.environ.get('PYBOSSA_OUTPUT', os.path.join(main_configs.BASE_DIR, "tmp", "results.json"))
TEMPLATE_FOLDER = os.environ.get('PYBOSSA_TEMPLATE_FOLDER', os.path.join(main_configs.BASE_DIR,
                                                                         "pybossa_importer", "templates"))
