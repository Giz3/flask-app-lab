import os
import json
from flask import flash, redirect, render_template, url_for, session
from . import posts_blueprint
from .forms import PostForm
from .utils import write_data



post_id = 0


@posts_blueprint.route("/add_post", methods=["GET", "POST"])
def create_post():
    """Додати новий пост."""
    global post_id

    form = PostForm()
    if form.validate_on_submit():

        username = session.get("user", "unauthorized")
        
        post_data = {
            "id": post_id,
            "title": form.title.data,
            "content": form.content.data,
            "category": form.category.data,
            "is_active": form.is_active.data,
            "publication_date": form.publish_date.data.isoformat(),
            "author": username
        }


        write_data(post_data)


        post_id += 1

        flash("Пост успішно додано!", "success")
        return redirect(url_for("posts.create_post"))

    return render_template("add_post.html", form=form)


@posts_blueprint.route("/", methods=["GET"])
def list_posts():
    """Показати всі пости."""
    posts = []

    try:

        file_path = os.path.join(os.path.dirname(__file__), 'data', 'posts.json')
        with open(file_path, "r", encoding="utf-8") as file:
            posts = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):

        posts = []

    return render_template("posts.html", posts=posts)