import sys
import os

from flask import Blueprint, render_template, request, redirect, url_for, session as flask_session
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import current_app

from models.Geral import Session
from models.User import User
from controllers.UserController import cadastrar_usuario 

views_bp = Blueprint('views_bp', __name__)

@views_bp.route("/")
def index():
    return redirect(url_for('views_bp.public_index'))

@views_bp.route("/public")
def public_index():
    print("template_folder:", current_app.template_folder)
    print("root_path:", current_app.root_path)
    print("searchpath:", current_app.jinja_loader.searchpath)
    return render_template("public/index.html")

@views_bp.route("/about")
def about():
    return render_template("public/about_us.html")

@views_bp.route("/contact")
def contact():
    return render_template("public/contact.html")

@views_bp.route("/dashboard")
def dashboard():
    if not flask_session.get("user_nome"):
        return redirect(url_for('views_bp.signin'))
    return render_template("admin/dashboard.html")

@views_bp.route("/signup")
def signup():
    return render_template("auth/signup.html")

@views_bp.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        db_session = Session()
        input_login = request.form.get("email", "").strip().lower()
        input_password = request.form.get("password", "").strip()

        from sqlalchemy import func
        user = db_session.query(User).filter(
            func.lower(User.login) == input_login
        ).first()

        db_session.close()

        if user and str(user.password).strip() == input_password:
            flask_session["user_id"] = user.id
            flask_session["user_nome"] = user.nome
            return redirect(url_for('views_bp.dashboard'))
        else:
            return render_template("auth/signin.html", error="Credenciais inválidas")

    return render_template("auth/signin.html")

@views_bp.route("/user/save", methods=["POST"])
def save_user():
    fullname = request.form.get("fullname")
    email = request.form.get("email")
    cpf_input = request.form.get("phone")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm-password")
    
    sucesso, resultado = cadastrar_usuario(fullname, email, cpf_input, password, confirm_password)
    
    if sucesso:
        db_session = Session()
        user = db_session.query(User).filter(User.login == email).first()
        if user:
            flask_session["user_id"] = user.id
            flask_session["user_nome"] = user.nome
        db_session.close()
        return redirect(url_for('views_bp.dashboard'))
    else:
        return render_template("auth/signup.html", error=resultado)
    
@views_bp.route('/auth_selection')
def auth_selection(): # O nome da função deve ser este
    return render_template('auth/auth_selection.html')

@views_bp.route("/profile")
def profile():
    if "user_id" not in flask_session:
        return redirect(url_for('views_bp.signin'))
    
    db_session = Session()
    user = db_session.query(User).filter(User.id == flask_session["user_id"]).first()
    db_session.close()
    
    return render_template("admin/profile.html", user=user)


@views_bp.route("/logout")
def logout():
    flask_session.clear()
    return redirect(url_for('views_bp.index'))

@views_bp.route("/delete_account", methods=["POST"])
def delete_account():
    if "user_id" not in flask_session:
        return redirect(url_for('views_bp.signin'))
    
    user_id = flask_session["user_id"]
    db_session = Session()
    user = db_session.query(User).filter(User.id == user_id).first()
    
    if user:
        db_session.delete(user)
        db_session.commit()
    
    db_session.close()
    flask_session.clear()
    return redirect(url_for('views_bp.index'))