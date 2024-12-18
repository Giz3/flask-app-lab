import json
import os


def write_data(data: dict):
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'posts.json')

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                posts = json.load(file)
            except json.JSONDecodeError:
                posts = []
    else:
        posts = []

    posts.append(data)

    with open(file_path, 'w') as file:
        json.dump(posts, file, indent=2)