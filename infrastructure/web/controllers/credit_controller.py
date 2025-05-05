from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from core.use_cases.credit_use_cases import GetUserBalanceUseCase
from core.repositories.credit_repository import CreditRepository
from core.repositories.user_repository import UserRepository
from infrastructure.ml.model_store import get_all_models

credit_bp = Blueprint("credit", __name__)

# Глобальные переменные для use cases
get_user_balance_use_case = None


def __init__(credit_repository: CreditRepository, user_repository: UserRepository):
    # Инициализация use cases
    global get_user_balance_use_case
    get_user_balance_use_case = GetUserBalanceUseCase(credit_repository)


@credit_bp.route("/balance")
def balance():
    if "user_id" not in session:
        flash("Пожалуйста, войдите в систему.", "warning")
        return redirect(url_for("user.login"))

    user_id = session["user_id"]
    balance = get_user_balance_use_case.execute(user_id)
    models = get_all_models()

    return render_template("balance.html", balance=balance, models=models,)
