
import functools
from sre_constants import SUCCESS

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from flask_login import login_manager, login_user
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired

from ..database.db import getDB
from ..models import auth


class RegisterForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField("username")
    password = PasswordField("password")
    rememberMe = BooleanField("Remember Me")


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        username = form.username.data
        password = form.password.data
        db = getDB()
        error = None
        print(username, password)
        flash("success")
        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        if error is None:
            try:
                model = auth.User()
                model.register(
                    username=username, password=password)
            except db.IntegrityError:
                error = f"User {username} is already taken."
            else:
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=("GET", "POST"))
def login():

    form = LoginForm()
    print((form.username.data, form.password.data))
    if form.validate_on_submit():
        print("hi")
        user = auth.User()
        success = user.login(form.username.data, form.password.data)
        # if success:
        #     flash(
        #         f"Login request for {form.username}, rememberMe = {form.rememberMe.data}")
        return redirect("/")
    print("login error")
    return render_template("auth/login.html", title="Login", form=form)


@bp.before_app_request
def loadLoggedUser():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        user = auth.User()
        g.user = user.gUser(str(user_id))


@bp.route("/logout")
def logout():
    session.clear()
    print("logged out")
    return redirect(url_for("auth.login"))


def loginRequired(view):
    @functools.wraps(view)
    def wrappedView(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrappedView
