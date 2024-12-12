import json
import os


def write_data(post_data: dict):
    """Записати новий пост у файл."""
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'posts.json')


    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                posts = json.load(file)
            except json.JSONDecodeError:
                posts = []
    else:
        posts = []


    posts.append(post_data)


    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(posts, file, indent=2, ensure_ascii=False)