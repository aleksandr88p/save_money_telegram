import json
import os

# Путь к файлу настроек
SETTINGS_FILE = 'data/user_settings.json'
# Загружаем настройки из файла
def load_user_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {}

# Сохраняем настройки в файл
def save_user_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

# Получаем язык пользователя
def get_user_language(user_id):
    settings = load_user_settings()
    return settings.get(str(user_id), 'english')  # По умолчанию — английский

# Устанавливаем язык пользователя
def set_user_language(user_id, language):
    settings = load_user_settings()
    settings[str(user_id)] = language
    save_user_settings(settings)
