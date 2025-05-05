# File: run.py
# Path: my_flask_app/run.py

from app import create_app
from flask import render_template

app = create_app()

@app.route('/')
def index():
    return render_template('index.html', title='Главная страница')

if __name__ == '__main__':
    app.run(debug=True)
