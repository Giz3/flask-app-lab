from app.users.views import users_bp  

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "Home page"

@app.route('/resume')
def resume():
    return render_template('resume.html', title="Резюме")

app.register_blueprint(users_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5001)