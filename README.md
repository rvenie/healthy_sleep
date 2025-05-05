
Core (Ядро):
- entities: Содержит бизнес-сущности (например, User), которые представляют основные объекты предметной области.
- use_cases: Содержит сценарии использования (бизнес-логику), которые описывают, как приложение должно работать.
- repositories: Определяет интерфейсы для работы с данными (например, UserRepository). Это абстракции, которые не зависят от конкретной реализации.


Infrastructure (Инфраструктура):
- db: Реализация репозиториев (например, UserRepositoryImpl), которая работает с базой данных.
- web: Веб-слой, который обрабатывает HTTP-запросы и взаимодействует с ядром через контроллеры.

Config (Конфигурация):
- main.py:  Точка входа в приложение, где инициализируются зависимости и запускается приложение.


│
├── core/
│ ├── entities/
│ │ ├── user.py
│ │ ├── model.py
│ │ └── prediction_log.py
│ ├── repositories/
│ │ ├── user_repository.py
│ │ ├── model_repository.py
│ │ └── log_repository.py
│ └── use_cases/
│ ├── user_use_cases.py
│ └── model_use_cases.py
│
├── infrastructure/
│ ├── db/
│ │ ├── base.py
│ │ ├── models.py
│ │ ├── user_repository_impl.py
│ │ ├── model_repository_impl.py
│ │ └── log_repository_impl.py
│ └── web/
│ └── controllers/
│ ├── user_controller.py
│ ├── model_controller.py
│ └── analytics_controller.py
│
├── config/
│ └── settings.py
│
├── main.py
└── requirements.txt


flask routes
Endpoint                 Methods    Rule
-----------------------  ---------  -----------------------
credit.balance           GET        /balance
index                    GET        /
prediction.predict       POST       /predict
prediction.predict_form  GET        /predict
static                   GET        /static/...
user.login               GET, POST  /login
user.logout              GET        /logout
user.profile             GET        /profile
user.register            GET, POST  /register