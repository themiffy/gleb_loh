from flask import Flask, render_template, request, jsonify
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import json


app = Flask(__name__)

HISTORY_FILE = Path("calculations_history.json")
# Создаём файл истории если его нет
if not HISTORY_FILE.exists():
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

def save_calculation(data):
    try:
        # Читаем существующую историю
        if HISTORY_FILE.stat().st_size == 0:
            history = []
        else:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)

        # Добавляем новую запись
        history.append(data)
        # Сортируем по убыванию коэффициента
        history.sort(key=lambda x: x["coefficient"], reverse=True)

        # Сохраняем обратно
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)

    except Exception as e:
        app.logger.error(f"Error saving calculation: {str(e)}")
        raise

@app.route("/save_calculation", methods=["POST"])
def save_calculation_route():
    try:
        data = request.json
        # Преобразуем коэффициент в float
        data["coefficient"] = float(data["coefficient"])
        save_calculation(data)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/get_history")
def get_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            if not content:
                return jsonify([])
            return jsonify(json.loads(content))
    except Exception as e:
        app.logger.error(f"Error loading history: {str(e)}")
        return jsonify([])

# Настройка отдельного логгера для сообщений
message_logger = logging.getLogger('messages')
message_logger.setLevel(logging.INFO)
handler = RotatingFileHandler(
    'messages.log',
    maxBytes=10000,
    backupCount=1,
    encoding='utf-8'
)
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
message_logger.addHandler(handler)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log_message', methods=['POST'])
def log_message():
    data = request.json
    message_logger.info(f"{data['name']}::: {data['message']}")
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)