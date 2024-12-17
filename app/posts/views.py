from flask import abort, flash, redirect, render_template, url_for, session
from . import posts_blueprint
from .forms import PostForm
from app.posts.models import Post
from app import db


@posts_blueprint.route("/add_post", methods=["GET", "POST"])
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        username = session.get("user", "unauthorized")

        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            is_active=form.is_active.data,
            posted=form.publish_date.data,
            author=username,
        )

        db.session.add(new_post)
        db.session.commit()

        flash("Post added successfully!", "success")
        return redirect(url_for("posts.add_post"))

    return render_template("add_post.html", form=form)


@posts_blueprint.route("/", methods=["GET"])
def show_posts():
    posts = Post.query.order_by(Post.posted.desc()).all()

    return render_template("posts.html", posts=posts)


@posts_blueprint.route("/post/<int:id>", methods=["GET"])
def view_post(id):
    post = Post.query.get(id)

    if post is None:
        abort(404)

    return render_template("post_details.html", post=post)


@posts_blueprint.route("/delete_post/<int:id>", methods=["POST"])
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()

    flash("Post deleted successfully!", "success")
    return redirect(url_for("posts.show_posts"))


@posts_blueprint.route("/edit_post/<int:id>", methods=["GET", "POST"])
def edit_post(id):
    post = Post.query.get_or_404(id)

    form = PostForm(obj=post)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.is_active.data
        post.posted = form.publish_date.data

        db.session.commit()

        flash("Post updated successfully!", "success")
        return redirect(url_for("posts.show_posts"))

    return render_template("edit_post.html", form=form, post=post)