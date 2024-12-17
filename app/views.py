from flask import render_template, current_app


@current_app.route("/")
def main():
    return render_template("home.html", page_title="Головна")


@current_app.route("/resume")
def resume():
    return render_template("resume.html", page_title="Моє резюме")


@current_app.route('/contact')
def contact():
    return render_template('contacts.html', page_title="Контакти")


@current_app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404