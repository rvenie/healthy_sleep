import os

# Путь к базе данных
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sleep_prediction.db")

# Путь к файлу с данными
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "Dry_Eye_Dataset.csv")

# Секретный ключ для сессий
SECRET_KEY = "your-secret-key-for-sessions"
