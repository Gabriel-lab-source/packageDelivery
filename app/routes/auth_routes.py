from app.extensions import db
from app.models.user import User
from flask import request, render_template, redirect, session, Blueprint, url_for, flash

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":
        user = User.query.filter_by(email=request.form.get("email")).first()

        if user and user.password == request.form.get("password"):
            session["user_id"] = user.id
            session["role"] = user.role
            return redirect("/")

        flash("Usuário ou senha não encontrado.", "danger")

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        role = request.form.get("role")

        new_user = User(
            name=request.form.get("name"),
            email=request.form.get("email"),
            password=request.form.get("password"),
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id
        session["role"] = new_user.role

        if role == "driver":
            return redirect("/create-driver")

        flash("Conta criada com sucesso!", "success")
        return redirect(url_for("main.home"))

    return render_template("register.html")


@auth_bp.route("/logout", methods=["GET"])
def logout():

    session.clear()
    return redirect(url_for("auth.login"))
