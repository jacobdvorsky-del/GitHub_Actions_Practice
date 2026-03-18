import pytest

from api.health_api import HealthAPI
from api.tasks_api import TasksAPI


def pytest_addoption(parser):
    parser.addoption(
        "--api-url",
        action="store",
        default="http://localhost:50090",
    )


@pytest.fixture
def base_url(request):
    return request.config.getoption("--api-url")


@pytest.fixture
def health_api(base_url):
    return HealthAPI(base_url)


@pytest.fixture
def tasks_api(base_url):
    return TasksAPI(base_url)


@pytest.fixture
def valid_task_data():
    return {
        "title": "This is Task Title",
        "description": "This is task description"
    }


@pytest.fixture
def updated_task_data():
    return {
        "title": "Updated title",
        "description": "Updated description"
    }


@pytest.fixture
def empty_task_data():
    return {}


@pytest.fixture
def create_task(tasks_api, valid_task_data):
    task_response = tasks_api.create_task(valid_task_data)
    yield task_response
    tasks_api.delete_task(task_response.json()["id"])


@pytest.fixture
def create_task_no_cleanup(tasks_api, valid_task_data):
    return tasks_api.create_task(valid_task_data)
