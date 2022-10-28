from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, redirect, render_template, url_for, request
from Constants import PSQL_KEY
from DatabaseCommands import DatabaseCommands
from SiteManager.wtforms_fields import LoginForm
from flask_login import LoginManager, current_user, login_user, logout_user
import models as M
from Constants import Flask_Secret_Key


db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder="SiteManager/Templates", static_folder="SiteManager/static")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = PSQL_KEY
    db.init_app(app)
    return app


# Configuration
app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = PSQL_KEY

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
    return render_template('home.html', username=username)


@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    # Allow login if validation success
    if login_form.validate_on_submit():
        user = M.AdminUser.get(login_form.username.data)
        login_user(user)
        return redirect(url_for('reg_requests'))

    return render_template("login_page.html", form=login_form)


@app.route("/logout", methods=['GET'])
def logout():
    logout_user()
    flash("You have logged out successfully")
    return redirect(url_for("home"))


@app.route("/regRequests", methods=['GET', 'POST'])
def reg_requests():
    print(current_user)
    if not current_user.is_authenticated:
        flash("Please login first")
        return redirect(url_for("login"))
    return render_template("register_requests_page.html")


@app.route("/register_request", methods=['POST'])
def register_requests():
    if request.method == 'POST':
        print("You requested something:")
        print(f'2 {request.json}')
        return 'Sent Successfully'
