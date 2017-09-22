from __future__ import print_function
from __future__ import unicode_literals

import json
import time

import pbclient

from configs.main_configs import LOGGER
from configs.pybossa_configs import ENDPOINT, API_KEY, PROJECT_CONFIGS, TASKS, REDUNDANCY, OUTPUT

pbclient.set('endpoint', ENDPOINT)
pbclient.set('api_key', API_KEY)


def create_project():
    """
    Create project on pybossa server.
    :return created project.
    """
    with open(PROJECT_CONFIGS, 'r'.encode("utf-8")) as f:
        configs = json.loads(f.read())
    result = pbclient.create_project(configs["name"], configs["short_name"], configs["description"])
    return result


def load_tasks(project_id, question="What is news tonality?"):
    """
    Load json tasks file to server for specified project.
    :param project_id project id.
    :param question: question for each task. Default is What is news tonality?
    """
    with open(TASKS, 'r'.encode("utf-8")) as f:
        data = json.loads(f.read())
    for obj in data:
        obj["question"] = question
        result = pbclient.create_task(project_id, obj, n_answers=REDUNDANCY)
        print(result)
        if isinstance(result, {}.__class__) \
                and result["status"] == "failed" \
                and result["exception_cls"] == "TooManyRequests":
            LOGGER.warning("Reach maximum requests per 15 minuets. Cant add more task. Suspend program for 15 minuets.")
            time.sleep(15 * 60)
            LOGGER.warning("Waking up. Resuming program.")
            pbclient.create_task(project_id, obj, n_answers=REDUNDANCY)


def export_results(project_id, limit, path=OUTPUT):
    """
    Export result as json.
    :param project_id: id of project.
    :param limit: taskruns limit.
    :param path path to outpit file
    """
    runs = pbclient.get_results(project_id, limit)
    with open(path, "w".encode("utf-8")) as f:
        json_string = json.dumps([ob.__dict__ for ob in runs])
        f.write(json_string)