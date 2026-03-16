from flask import Blueprint, jsonify, request

task_bp = Blueprint("tasks", __name__)

tasks = []
state = {"task_id_counter": 1}

@task_bp.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks), 200

@task_bp.route("/tasks/<int:id>", methods=["GET"])
def get_task(id):
    task = next((t for t in tasks if t["id"] == id), None)
    if task is None:
        return jsonify({"message": "task not found"}), 404
    return jsonify(task), 200

@task_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or "title" not in data or data["title"] == "":
        return jsonify({"message":"title is required"}),400
    task = {
        "id": state["task_id_counter"],
        "title": data["title"],
        "description": data["description"]
    }
    tasks.append(task)
    state["task_id_counter"] += 1
    return jsonify(task), 201

@task_bp.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    task = next((t for t in tasks if t["id"] == id), None)
    if task is None:
        return jsonify({"message": "task not found"}), 404
    data = request.get_json()
    task["title"] = data.get("title", task["title"])
    task["description"] = data.get("description", task["description"])
    return jsonify(task), 200

@task_bp.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = next((t for t in tasks if t["id"] == id), None)
    if task is None:
        return jsonify({"message": "task does not exist"}), 404
    tasks.remove(task)
    return jsonify({"message": "task deleted"}), 200
    