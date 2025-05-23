from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from core.use_cases.credit_use_cases import GetUserBalanceUseCase, AddCreditsUseCase
from core.repositories.credit_repository import CreditRepository
from core.repositories.user_repository import UserRepository
from infrastructure.ml.model_store import get_all_models

credit_bp = Blueprint("credit", __name__)

# Глоб
get_user_balance_use_case = None
add_credits_use_case = None

def __init__(credit_repository: CreditRepository, user_repository: UserRepository):
    global get_user_balance_use_case, add_credits_use_case
    get_user_balance_use_case = GetUserBalanceUseCase(credit_repository)
    add_credits_use_case = AddCreditsUseCase(credit_repository, user_repository)

@credit_bp.route("/balance")
def balance():
    if "user_id" not in session:
        flash("Пожалуйста, войдите в систему.", "warning")
        return redirect(url_for("user.login"))

    user_id = session["user_id"]
    balance = get_user_balance_use_case.execute(user_id)
    models = get_all_models()

    return render_template("balance.html", balance=balance, models=models,)

@credit_bp.route("/add_credits", methods=["POST"])
def add_credits():
    if "user_id" not in session:
        flash("Пожалуйста, войдите в систему.", "warning")
        return redirect(url_for("user.login"))

    user_id = session["user_id"]
    credits_amount = request.form.get("credits_amount", type=int, default=0)
    
    # Валидация
    if credits_amount <= 0:
        flash("Пожалуйста, введите положительное число кредитов.", "warning")
        return redirect(url_for("credit.balance"))
    
    # Пополнение
    add_credits_use_case.execute(user_id, credits_amount, "manual_add")
    
    flash(f"Ваш баланс успешно пополнен на {credits_amount} кредитов!", "success")
    return redirect(url_for("credit.balance"))
