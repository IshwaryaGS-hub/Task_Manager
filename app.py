from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Load tasks
def load_tasks():
    if not os.path.exists("tasks.json"):
        return []
    with open("tasks.json", "r") as f:
        return json.load(f)

# Save tasks
def save_tasks(tasks):
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)


@app.route("/")
def home():
    filter_type = request.args.get("filter", "all")
    tasks = load_tasks()

    if filter_type == "active":
        tasks = [t for t in tasks if not t["completed"]]
    elif filter_type == "completed":
        tasks = [t for t in tasks if t["completed"]]

    return render_template("index.html", tasks=tasks, filter_type=filter_type)


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("task")
    priority = request.form.get("priority")

    if title:
        tasks = load_tasks()
        tasks.append({
            "title": title,
            "completed": False,
            "priority": priority
        })
        save_tasks(tasks)

    return redirect(url_for("home"))


@app.route("/toggle/<int:index>")
def toggle_task(index):
    tasks = load_tasks()
    tasks[index]["completed"] = not tasks[index]["completed"]
    save_tasks(tasks)
    return redirect(url_for("home"))


@app.route("/delete/<int:index>")
def delete_task(index):
    tasks = load_tasks()
    tasks.pop(index)
    save_tasks(tasks)
    return redirect(url_for("home"))


@app.route("/edit/<int:index>", methods=["POST"])
def edit_task(index):
    new_title = request.form.get("new_title")
    new_priority = request.form.get("new_priority")

    tasks = load_tasks()
    tasks[index]["title"] = new_title
    tasks[index]["priority"] = new_priority

    save_tasks(tasks)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
