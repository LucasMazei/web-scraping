from flask import Flask, render_template, flash, redirect, url_for, request, send_file, make_response, jsonify
from app import app
from modules.__init__ import db, login_manager
from modules.models.forms import LoginForm, RegisterForm, RegisterDish
from modules.models.tables import Waiter, Tables, Dish
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.exceptions import BadRequest
from werkzeug.utils import secure_filename
from modules.models.forms import RegisterDish, RegisterForm, LoginForm


@app.route('/', methods=['GET'])
def index():
    import requests
    data = requests.get(
        "https://economia.awesomeapi.com.br/all")
    td = list(data.json().keys())
    tr = [key for key in data.json()[td[0]].keys()]
    return render_template('index.html', data=data.json(), tr=tr, td=td)


@app.route('/index')
def redirect_to_index():
    return redirect(url_for("index"))


@login_manager.user_loader
def load_user(id):
    return Waiter.query.filter_by(id=id).first()
    # return User.get_id(User.query.filter_by(id=id).first())


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Waiter.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Logado com sucesso!")
            if user.username == 'adm':
                return redirect(url_for("index"))
            else:
                return redirect(url_for("index"))
        else:
            flash("Login inválido!")
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("Até mais!")
    return redirect(url_for("index"))


@app.route("/cadastro", methods=["GET", "POST"])
def waiter_register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = generate_password_hash(form.password.data)
        name = form.name.data
        email = form.email.data
        try:
            new_user = Waiter(username, password, name, email)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            flash('Ocorreu um erro, verifique os dados e tente novamente.')
    return render_template('waiter_register.html', form=form)


@app.route("/get_request/")
def get_response(user_selected=False, methods=['GET']):
    myDict = Waiter.getUser(user_selected)
    return jsonify(myDict)


@app.route("/post_request/<username>/<password>/<name>/<email>")
def post_request(username="", password="", name="", email="", methods=['POST']):
    password = generate_password_hash(password)
    try:
        new_user = Waiter(username, password, name, email)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(Waiter.getUser(username))
    except Exception as e:
        dict_error = {"erro": str(e)}
        return jsonify(dict_error)
