import os

# Корневая директория проекта
base_dir = "my_flask_app"

# Список директорий для создания
directories = [
    os.path.join(base_dir, "app"),
    os.path.join(base_dir, "app", "student"),
    os.path.join(base_dir, "app", "teacher"),
    os.path.join(base_dir, "app", "admin"),
    os.path.join(base_dir, "migrations")
]

# Создание директорий
for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"Создана директория: {directory}")

# Файлы и их базовое содержимое (без заголовка)
files = {
    os.path.join(base_dir, "app", "__init__.py"): "# Инициализация приложения и подключение расширений\n",
    os.path.join(base_dir, "app", "config.py"): "# Конфигурация (SECRET_KEY, параметры БД, настройки Flask-Mail и др.)\n",
    os.path.join(base_dir, "app", "models.py"): "# Определение моделей (User, Course, Registration, PortfolioItem, Review, TheatreShow и т.д.)\n",
    os.path.join(base_dir, "app", "forms.py"): "# Формы (регистрация, логин, изменение профиля, запись на курс и проч.)\n",
    os.path.join(base_dir, "app", "email.py"): "# Логика формирования и отправки email (подтверждение регистрации, восстановление пароля)\n",
    os.path.join(base_dir, "app", "student", "__init__.py"): "# Blueprint для функционала студентов/посетителей\n",
    os.path.join(base_dir, "app", "student", "routes.py"): "# Маршруты (регистрация, профиль, расписание, запись на курсы, портфолио, история, отзывы)\n",
    os.path.join(base_dir, "app", "teacher", "__init__.py"): "# Blueprint для функционала преподавателя\n",
    os.path.join(base_dir, "app", "teacher", "routes.py"): "# Маршруты (просмотр курсов, список студентов, управление записями студентов)\n",
    os.path.join(base_dir, "app", "admin", "__init__.py"): "# Blueprint для административного функционала\n",
    os.path.join(base_dir, "app", "admin", "routes.py"): "# Маршруты (управление данными о представлениях, курсах, преподавателях, студентах; модерация отзывов)\n",
    os.path.join(base_dir, "run.py"): "# Точка входа для запуска приложения\n"
}

# Создание файлов с заголовком (имя файла и путь)
for file_path, content in files.items():
    # Заголовок файла
    header = f"# File: {os.path.basename(file_path)}\n# Path: {file_path}\n\n"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(header + content)
    print(f"Создан файл: {file_path}")
