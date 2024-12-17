from datetime import timedelta

from flask import (render_template,
                   request,
                   url_for,
                   redirect,
                   flash,
                   session,
                   make_response)
from werkzeug.security import check_password_hash, generate_password_hash

from . import users_blueprint


@users_blueprint.route('/hi/<string:name>')
def greetings(name):
    name = name.upper()
    age = request.args.get("age", type=int)
    return render_template("hi.html", name=name, age=age)


@users_blueprint.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator",
                     age=19, _external=True)
    return redirect(to_url)


@users_blueprint.route("/users/login", methods=["GET", "POST"])
def login():
    correct_username = "admin"
    correct_password = generate_password_hash("password123")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        is_username_correct = username == correct_username
        is_password_correct = check_password_hash(correct_password, password)

        if is_username_correct and is_password_correct:
            session["user"] = username
            flash("Login successful!", "success")
            return redirect(url_for("users.profile", name=username))
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html")


@users_blueprint.route("/profile", methods=["GET", "POST"])
def profile():
    if "user" not in session:
        flash("You need to log in to view this page.", "warning")
        return redirect(url_for("users.login"))

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add":
            key = request.form.get("key")
            value = request.form.get("value")
            days = request.form.get("days", type=int)

            if key and value and days:
                response = make_response(redirect(url_for("users.profile")))
                response.set_cookie(key, value, max_age=timedelta(days=days))
                flash(f"Cookie '{key}' added successfully!", "success")
                return response
            else:
                flash_message = (
                        "Please provide a valid key, "
                        "value and expiration days."
                )
                flash(flash_message, "danger")
        elif action == "delete_key":
            key = request.form.get("delete_key")
            response = make_response(redirect(url_for("users.profile")))
            response.set_cookie(key, "", expires=0)
            flash(f"Cookie '{key}' deleted successfully!", "success")
            return response

        elif action == "delete_all":
            response = make_response(redirect(url_for("users.profile")))
            for cookie_key in request.cookies.keys():
                response.set_cookie(cookie_key, "", expires=0)
            flash("All cookies deleted successfully!", "success")
            return response

    current_cookies = request.cookies.to_dict()
    return render_template("profile.html", username=session["user"],
                           cookies=current_cookies)


@users_blueprint.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    flash("You have benn logged out.", "info")
    return redirect(url_for("users.login"))


@users_blueprint.route("/set_color_scheme/<string:scheme>")
def set_color_scheme(scheme):
    if scheme not in ["light", "dark"]:
        flash("Invalid color scheme selected.", "danger")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie("color_scheme", scheme, max_age=timedelta(days=30))
    flash(f"Color scheme set to {scheme.capitalize()}!", "success")
    return response