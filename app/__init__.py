from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response

def create_app():
    app = Flask(__name__)
    app.secret_key = 'supersecretkey'

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        valid_user = {'username': 'admin', 'password': 'password123'}

        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            if username == valid_user['username'] and password == valid_user['password']:
                session['user'] = username
                flash('Успішний вхід!', 'success')
                return redirect(url_for('profile'))
            else:
                flash('Невірні облікові дані. Спробуйте ще раз.', 'error')

        return render_template('login.html')

    @app.route('/profile', methods=['GET', 'POST'])
    def profile():
        if 'user' not in session:
            flash('Будь ласка, увійдіть, щоб переглянути профіль.', 'error')
            return redirect(url_for('login'))

        username = session['user']
        theme = request.cookies.get('theme', 'light')  # Значення за замовчуванням — світла тема

        response = make_response(render_template('profile.html', username=username, theme=theme))

        if request.method == 'POST' and 'add_cookie' in request.form:
            key = request.form['key']
            value = request.form['value']
            max_age = int(request.form['max_age']) if request.form['max_age'] else None

            if key and value:
                response.set_cookie(key, value, max_age=max_age)
                flash(f'Кукі "{key}" успішно додано.', 'success')
            else:
                flash('Будь ласка, введіть ключ і значення для кукі.', 'error')

        if request.method == 'POST' and 'delete_cookie' in request.form:
            key = request.form['delete_key']
            if key:
                response.delete_cookie(key)
                flash(f'Кукі "{key}" успішно видалено.', 'success')
            else:
                flash('Будь ласка, введіть ключ кукі для видалення.', 'error')

        if request.method == 'POST' and 'delete_all_cookies' in request.form:
            for key in request.cookies.keys():
                response.delete_cookie(key)
            flash('Усі кукі успішно видалено.', 'success')

        return response

    @app.route('/set_theme/<theme>')
    def set_theme(theme):
        if theme not in ['light', 'dark']:
            flash("Невірна тема! Доступні варіанти: світла або темна.", "error")
            return redirect(url_for('profile'))

        # Встановлення кукі для теми
        response = make_response(redirect(url_for('profile')))
        response.set_cookie('theme', theme, max_age=30 * 24 * 60 * 60)  # Кукі діють 30 днів
        flash(f"Тема змінена на {'світлу' if theme == 'light' else 'темну'}.", "success")
        return response

    @app.route('/logout')
    def logout():
        session.pop('user', None)
        flash('Ви вийшли з профілю.', 'info')
        return redirect(url_for('login'))

    return app