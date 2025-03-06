from flask import Flask, render_template, request, jsonify
import logging
from datetime import datetime

app = Flask(__name__)

# Настройка логгера для сообщений
logging.basicConfig(
    filename='messages.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log_message', methods=['POST'])
def log_message():
    data = request.json
    log_entry = f"Сообщение от {data['name']}: {data['message']}"
    app.logger.info(log_entry)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)