from flask import render_template, Blueprint, session

main_bp = Blueprint(
    "main",
    __name__,
    url_prefix="/main"
)


@main_bp.route("/")
def home():
    print(session)
    return render_template("home.html")


@main_bp.route("/health")
def health():
    return {"status": "ok"}
