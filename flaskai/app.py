from flask import Flask, request, jsonify
import sqlite3
from openai import OpenAI

# === CONFIG ===
API_KEY = "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"
client = OpenAI(api_key=API_KEY)

DATABASE = "quiz.db"
app = Flask(__name__)

# === DATABASE INIT ===
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS antwoorden (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vraag TEXT,
                    antwoord TEXT,
                    correct BOOLEAN
                )''')
    conn.commit()
    conn.close()

# === ROUTES ===

@app.route('/vraag', methods=['GET'])
def vraag():
    prompt = (
        "Genereer één waar of onwaar vraag over het Beatrix Kinderziekenhuis in Groningen. "
        "De vraag moet geschikt zijn voor kinderen en begrijpelijk zijn voor een leeftijd tussen 6 en 12 jaar. "
        "Geef je antwoord uitsluitend in JSON-formaat zoals dit voorbeeld:\n"
        "{'vraag': 'Het Beatrix Kinderziekenhuis ligt in Groningen.', 'correcte_antwoord': 'waar'}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        output = response.choices[0].message.content.strip()

        # Probeer de gegenereerde tekst als Python dict te parsen
        data = eval(output)  # alleen doen omdat GPT een string-formaat JSON teruggeeft
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": "OpenAI-fout", "details": str(e)}), 500

@app.route('/antwoord', methods=['POST'])
def antwoord():
    data = request.get_json()
    vraag = data['vraag']
    antwoord = data['antwoord'].lower()
    correct = data['correct'].lower()
    is_correct = antwoord == correct

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO antwoorden (vraag, antwoord, correct) VALUES (?, ?, ?)",
              (vraag, antwoord, is_correct))
    conn.commit()
    conn.close()

    return jsonify({"status": "opgeslagen", "correct_beantwoord": is_correct})

@app.route('/resultaten', methods=['GET'])
def resultaten():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT vraag, antwoord, correct FROM antwoorden")
    rows = c.fetchall()
    conn.close()
    return jsonify([{"vraag": r[0], "antwoord": r[1], "correct": r[2]} for r in rows])

# === MAIN ===
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
