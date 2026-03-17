
def test_get_tasks_returns_status_code_200(tasks_api):
    response = tasks_api.get_tasks()
    assert response.status_code == 200


def test_create_task_returns_status_code_201(tasks_api, valid_task_data):
    response = tasks_api.create_task(valid_task_data)
    assert response.status_code == 201


def test_create_task_with_invalid_data_returns_status_code_400(tasks_api, empty_task_data):
    response = tasks_api.create_task(empty_task_data)
    assert response.status_code == 400


def test_create_task_with_invalid_data_returns_error_message(tasks_api, empty_task_data):
    response = tasks_api.create_task(empty_task_data)
    assert response.json()["message"] == "title is required"


def test_get_task_returns_status_code_200(tasks_api, create_task):
    response = tasks_api.get_task(create_task.json()["id"])
    assert response.status_code == 200


def test_get_task_returns_correct_task_by_id(tasks_api, create_task, valid_task_data):
    response = tasks_api.get_task(create_task.json()["id"])
    assert response.json()["title"] == valid_task_data["title"]
    assert response.json()["description"] == valid_task_data["description"]


def test_get_task_with_invalid_id_returns_404_status_code(tasks_api):
    response = tasks_api.get_task(9999)
    assert response.status_code == 404


def test_update_task_returns_status_code_200(tasks_api, create_task, updated_task_data):
    response = tasks_api.update_task(create_task.json()["id"], updated_task_data)
    assert response.status_code == 200


def test_update_task_returns_updated_data(tasks_api, create_task, updated_task_data):
    response = tasks_api.update_task(create_task.json()["id"], updated_task_data)
    assert response.json()["title"] == updated_task_data["title"]
    assert response.json()["description"] == updated_task_data["description"]


def test_delete_task_returns_status_code_200(tasks_api, create_task_no_cleanup):
    response = tasks_api.delete_task(create_task_no_cleanup.json()["id"])
    assert response.status_code == 200


def test_get_task_that_id_deleted_returns_404(tasks_api, create_task_no_cleanup):
    task_id = create_task_no_cleanup.json()["id"]
    tasks_api.delete_task(task_id)
    response = tasks_api.get_task(task_id)
    assert response.status_code == 404
