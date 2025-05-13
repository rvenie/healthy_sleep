from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from core.use_cases.prediction_use_cases import MakePredictionUseCase
from core.repositories.user_repository import UserRepository
from core.repositories.model_repository import ModelRepository
from core.use_cases.credit_use_cases import DeductCreditsUseCase
from infrastructure.ml.model_store import get_all_models, get_feature_names

prediction_bp = Blueprint("prediction", __name__)

# Глобальные переменные для use cases
make_prediction_use_case = None
deduct_credits_use_case = None


def __init__(user_repository: UserRepository, model_repository: ModelRepository,
             prediction_repository, credit_repository):
    # Инициализация use cases
    global make_prediction_use_case, deduct_credits_use_case
    deduct_credits_use_case = DeductCreditsUseCase(credit_repository, user_repository)
    make_prediction_use_case = MakePredictionUseCase(
        prediction_repository,
        model_repository,
        deduct_credits_use_case
    )
    prediction_bp.user_repository = user_repository


@prediction_bp.route("/predict", methods=["GET"])
def predict_form():
    if "user_id" not in session:
        flash("Пожалуйста, войдите в систему.", "warning")
        return redirect(url_for("user.login"))

    # Получаем пользователя по ID
    user_id = session["user_id"]
    user = prediction_bp.user_repository.get_by_id(user_id)

    # Получаем список моделей и список признаков
    models = get_all_models()
    features = get_feature_names()

    return render_template(
        "predict.html",
        models=models,
        features=features,
        credits=user.credits  # Передаем количество кредитов в шаблон
    )


@prediction_bp.route("/predict", methods=["POST"])
def predict():
    if "user_id" not in session:
        flash("Пожалуйста, войдите в систему.", "warning")
        return redirect(url_for("user.login"))

    user_id = session["user_id"]
    model_id = int(request.form.get("model_id"))

    # Собираем входные данные из формы
    input_data = {}
    for field_name, value in request.form.items():
        if field_name != "model_id" and field_name != "csrf_token":
            # Преобразуем числовые значения из строк
            if value.replace(".", "", 1).isdigit():
                if "." in value:
                    input_data[field_name] = float(value)
                else:
                    input_data[field_name] = int(value)
            else:
                input_data[field_name] = value

    try:
        # Выполняем предсказание
        prediction = make_prediction_use_case.execute(user_id, model_id, input_data)
        flash(f"Предсказанное качество сна: {prediction.prediction_result}", "success")
        user = prediction_bp.user_repository.get_by_id(user_id)
        return render_template(
            "prediction_result.html",
            prediction=prediction,
            credits=user.credits
        )
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("prediction.predict_form"))
