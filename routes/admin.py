from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session as flask_session

from repositories.admin_repository import AdminRepository

admin_bp = Blueprint("admin_bp", __name__)


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not flask_session.get("admin_id"):
            return redirect(url_for("admin_bp.admin_login"))
        return f(*args, **kwargs)
    return wrapper


@admin_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        admin = AdminRepository.authenticate(
            request.form.get("email"), request.form.get("password")
        )
        if admin:
            flask_session["admin_id"] = admin["id"]
            flask_session["admin_nome"] = admin["nome"]
            return redirect(url_for("admin_bp.list_admins"))
        return render_template("auth/signin.html", error="Credenciais inválidas")
    return render_template("auth/signin.html")


@admin_bp.route("/admin/logout")
def admin_logout():
    flask_session.pop("admin_id", None)
    flask_session.pop("admin_nome", None)
    return redirect(url_for("views_bp.index"))


@admin_bp.route("/admin/admins")
@admin_required
def list_admins():
    return render_template("admin/admins/list.html", admins=AdminRepository.list_all())


@admin_bp.route("/admin/admins/new", methods=["GET", "POST"])
@admin_required
def create_admin():
    if request.method == "POST":
        data = request.form.to_dict()
        data["ativo"] = "ativo" in request.form
        ok, result = AdminRepository.create(data)
        if ok:
            flash("Admin criado com sucesso!", "success")
            return redirect(url_for("admin_bp.list_admins"))
        return render_template("admin/admins/form.html", admin=data, error=result, editing=False)
    return render_template("admin/admins/form.html", admin={"ativo": True}, editing=False)


@admin_bp.route("/admin/admins/<int:admin_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_admin(admin_id):
    admin = AdminRepository.find_by_id(admin_id)
    if not admin:
        flash("Admin não encontrado.", "error")
        return redirect(url_for("admin_bp.list_admins"))

    if request.method == "POST":
        data = request.form.to_dict()
        data["ativo"] = "ativo" in request.form
        ok, result = AdminRepository.update(admin_id, data)
        if ok:
            flash("Admin atualizado!", "success")
            return redirect(url_for("admin_bp.list_admins"))
        data["id"] = admin_id
        return render_template("admin/admins/form.html", admin=data, error=result, editing=True)

    return render_template("admin/admins/form.html", admin=admin, editing=True)


@admin_bp.route("/admin/admins/<int:admin_id>/delete", methods=["POST"])
@admin_required
def delete_admin(admin_id):
    if admin_id == flask_session.get("admin_id"):
        flash("Você não pode excluir a própria conta.", "error")
    elif AdminRepository.delete(admin_id):
        flash("Admin excluído.", "success")
    else:
        flash("Admin não encontrado.", "error")
    return redirect(url_for("admin_bp.list_admins"))