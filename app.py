from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, redirect, render_template, url_for, g
from Constants import PSQL_KEY
from DatabaseCommands import DatabaseCommands
from SiteManager.wtforms_fields import LoginForm
from flask_login import LoginManager, current_user, login_user, logout_user
import models as M
from Constants import Flask_Secret_Key
import flask_sijax
import os


db = SQLAlchemy()
path = os.path.join('.', os.path.dirname(__file__), 'SiteManager/static/js/sijax/')


def create_app():
    app = Flask(__name__, template_folder="SiteManager/Templates", static_folder="SiteManager/static")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = PSQL_KEY
    db.init_app(app)
    return app


# Configuration
app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = PSQL_KEY
app.config['SIJAX_STATIC_PATH'] = path
app.config['SIJAX_JSON_URI'] = 'SiteManager/static/js/sijax/json2.js'
flask_sijax.Sijax(app)

db_command = DatabaseCommands(db)
app.config['SECRET_KEY'] = Flask_Secret_Key


# config flask login
login = LoginManager(app)
login.init_app(app)


@login.user_loader
def load_user(user_id: str):
    return M.AdminUser.get(user_id)


@app.route('/', methods=['GET'])
def home():
    username = "Fake Username"
    if current_user.is_authenticated:
        username = current_user.id

    return render_template('home.html', username=username, current_user=current_user)


@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    # Allow login if validation success
    if login_form.validate_on_submit():
        user = M.AdminUser.get(login_form.username.data)
        login_user(user)
        return redirect(url_for('home'))

    return render_template("login_page.html", form=login_form, current_user=current_user)


@app.route("/logout", methods=['GET'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("You have logged out successfully")
    return redirect(url_for("home"))


# @app.route("/regRequests", methods=['GET', 'POST'])
@flask_sijax.route(app, '/regRequests')
def reg_requests():
    if not current_user.is_authenticated:
        flash("Please login first")
        return redirect(url_for("login"))

    # Takes all register requests from db
    with app.app_context():
        registerRequests = db_command.get_all_register_requests()

    def accept_server_request(obj_response, html_name):
        register_id = int(html_name.split('accept-btn-')[1])
        register_obj = list(filter(lambda request: request.register_id == register_id, registerRequests))
        if len(register_obj) == 1:
            register_obj = register_obj[0]

            # Add new user and remove user request
            db_command.add_user(register_obj)
            db_command.remove_register_request(register_obj.register_id)
            flash(f"{register_obj.first_name} {register_obj.last_name} have been accepted")
        # Refresh page
        obj_response.script("location.reload()")

    def decline_server_request(obj_response, html_name):
        register_id = int(html_name.split('decline-btn-')[1])
        db_command.remove_register_request(register_id)  # Remove register request

        # Flash Response
        register_obj = list(filter(lambda request: request.register_id == register_id, registerRequests))
        if len(register_obj) == 1:
            register_obj = register_obj[0]
            flash(f"{register_obj.first_name} {register_obj.last_name} have been decline")
        # Refresh page
        obj_response.script("location.reload()")

    if g.sijax.is_sijax_request:
        g.sijax.register_callback('accept_server_request', accept_server_request)
        g.sijax.register_callback('decline_server_request', decline_server_request)
        return g.sijax.process_request()

    return render_template("register_requests_page.html", current_user=current_user, registerRequests=registerRequests)
