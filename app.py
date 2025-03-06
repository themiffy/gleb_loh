from flask import Flask, render_template, request, jsonify
import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)

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