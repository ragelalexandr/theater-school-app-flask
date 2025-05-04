# utils.py

import os
import secrets
from flask import current_app
from werkzeug.utils import secure_filename

def save_picture(form_picture):
    # Генерируем уникальное имя для избежания конфликтов
    random_hex = secrets.token_hex(8)
    # Извлекаем расширение из имени файла, используя secure_filename для безопасности
    _, file_ext = os.path.splitext(secure_filename(form_picture.filename))
    picture_filename = random_hex + file_ext
    # Определяем путь сохранения: убедитесь, что папка static/profile_pics существует
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_filename)
    
    # Сохраняем файл по сформированному пути
    form_picture.save(picture_path)
    
    return picture_filename
