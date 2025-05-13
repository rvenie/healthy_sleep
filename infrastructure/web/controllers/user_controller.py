from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from core.use_cases.user_use_cases import UserRegistrationUseCase, UserAuthenticationUseCase
from core.repositories.user_repository import UserRepository
from core.use_cases.prediction_use_cases import GetUserPredictionsUseCase
import json
user_bp = Blueprint("user", __name__)


def __init__(user_repository: UserRepository, prediction_repository):
    global user_registration_use_case, user_authentication_use_case, get_user_predictions_use_case
    user_registration_use_case = UserRegistrationUseCase(user_repository)
    user_authentication_use_case = UserAuthenticationUseCase(user_repository)
    get_user_predictions_use_case = GetUserPredictionsUseCase(prediction_repository)
    user_bp.user_repository = user_repository



@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        try:
            user = user_registration_use_case.execute(username, password, email)
            flash("Регистрация успешна! Теперь вы можете войти.", "success")
            return redirect(url_for("user.login"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("register.html")


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            user = user_authentication_use_case.execute(username, password)
            session["user_id"] = user.id
            session["username"] = user.username
            flash(f"Добро пожаловать, {user.username}!", "success")
            return redirect(url_for("prediction.predict_form"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("login.html")


@user_bp.route("/logout")
def logout():
    session.clear()
    flash("Вы вышли из системы.", "info")
    return redirect(url_for("user.login"))


@user_bp.route("/profile")
def profile():
    if "user_id" not in session:
        flash("Пожалуйста, войдите в систему.", "warning")
        return redirect(url_for("user.login"))

    user_id = session["user_id"]
    user = user_bp.user_repository.get_by_id(user_id)
    
    # История предиктов
    predictions = get_user_predictions_use_case.execute(user_id)
    
    for prediction in predictions:
        if isinstance(prediction.input_data, str):
            try:
                prediction.input_data = json.loads(prediction.input_data)
            except json.JSONDecodeError:
                pass
    
    return render_template("profile.html", user=user, predictions=predictions)


