from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from models import Weetje

Question_bp = Blueprint('question', __name__, template_folder='templates')

# ─── Module‐level state (one session only) ───────────────────
question_ids = []
current_idx = 0
current_answer = None
current_is_good = None
# ──────────────────────────────────────────────────────────────

@Question_bp.route('/start')
def start():
    global question_ids, current_idx, current_answer, current_is_good
    # load all question IDs in order
    question_ids = [w.id for w in Weetje.query.order_by(Weetje.id).all()]
    current_idx = 0
    current_answer = None
    current_is_good = None
    return render_template('Question/start.html')

@Question_bp.route('/question')
def question():
    global current_idx, question_ids
    # if we’ve run out of questions, go to end
    if current_idx >= len(question_ids):
        return redirect(url_for('question.end'))
    q = Weetje.query.get_or_404(question_ids[current_idx])
    return render_template('Question/question.html', question=q)

@Question_bp.route('/answer', methods=['GET', 'POST'])
def answer():
    """
    GET  → polled by the browser to see if Pico has answered yet
    POST → called by your Pico: JSON { "response": "waar" } or { "response": "nietwaar" }
    """
    global current_idx, current_answer, current_is_good

    if request.method == 'POST' and request.is_json:
        data = request.get_json()
        resp = data.get('response')  # “waar” or “nietwaar”
        # grade against the DB field `gender`
        q = Weetje.query.get_or_404(question_ids[current_idx])
        current_answer = resp
        current_is_good = (resp == q.gender)
        # advance for next time
        current_idx += 1
        return jsonify(status='ok')

    # GET path: tell the page whether we have an answer yet
    return jsonify(
        has_answer = current_answer is not None,
        response   = current_answer,
        is_good    = current_is_good
    )

@Question_bp.route('/end')
def end():
    return render_template('Question/end.html')

@Question_bp.route('/health')
def health():
    return jsonify(status='ok')