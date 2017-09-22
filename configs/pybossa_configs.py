import main_configs
import os

"""
Pybossa related configs.
"""
ENDPOINT = os.environ.get('PYBOSSA_ENDPOINT', 'http://localhost:5000')
API_KEY = os.environ.get('PYBOSSA_KEY', '1f2f4fe0-d576-42d4-bdf6-8193cec5fc0e')
PROJECT_CONFIGS = os.environ.get('PYBOSSA_PROJECT', os.path.join(main_configs.BASE_DIR, "configs/project.json"))
TASKS = os.environ.get('PYBOSSA_TASKS', os.path.join(main_configs.BASE_DIR, "tmp/reuters.json"))
REDUNDANCY = os.environ.get('PYBOSSA_REDUNDANCY', 3)
OUTPUT = os.environ.get('PYBOSSA_OUTPUT',  os.path.join(main_configs.BASE_DIR, "tmp/results.json"))
TEMPLATE_FOLDER = os.environ.get('PYBOSSA_TEMPLATE_FOLDER', os.path.join(main_configs.BASE_DIR, "templates/"))
