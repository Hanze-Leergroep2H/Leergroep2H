# server.py
from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB = 'quiz.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            question TEXT,
            answer TEXT,
            correct_answer TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    user_id = data.get("user_id")
    question = data.get("question")
    answer = data.get("answer")
    correct_answer = data.get("correct_answer")
    timestamp = datetime.now().isoformat()

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        INSERT INTO quiz_results (user_id, question, answer, correct_answer, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, question, answer, correct_answer, timestamp))
    conn.commit()
    conn.close()

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=5000)
