from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from models import Weetje
import random

Question_bp = Blueprint('question', __name__, template_folder='templates')

# ─── Module‐level state (voor één enkele client) ────────────────
question_ids = []
current_idx = 0
current_answer = None
current_is_good = None
answered_this_round = False
# ────────────────────────────────────────────────────────────────

@Question_bp.route('/start')
def start():
    global question_ids, current_idx, current_answer, current_is_good, answered_this_round

    # Haal alle weetje IDs op en schud ze door elkaar
    question_ids = [w.id for w in Weetje.query.with_entities(Weetje.id).all()]
    random.shuffle(question_ids)

    current_idx = 0
    current_answer = None
    current_is_good = None
    answered_this_round = False

    return render_template('Question/start.html')


@Question_bp.route('/question')
def question():
    global current_idx, question_ids, current_answer, current_is_good, answered_this_round

    if current_idx >= len(question_ids):
        return redirect(url_for('question.end'))

    # Reset answer status voor deze ronde
    current_answer = None
    current_is_good = None
    answered_this_round = False

    q = Weetje.query.get_or_404(question_ids[current_idx])
    return render_template('Question/question.html', question=q)


@Question_bp.route('/answer', methods=['GET', 'POST'])
def answer():
    global current_idx, question_ids, current_answer, current_is_good, answered_this_round

    if request.method == 'POST' and request.is_json:
        if answered_this_round or current_idx >= len(question_ids):
            return jsonify(status='ignored')  # Voorkom dubbel antwoorden

        data = request.get_json()
        resp = data.get('response')  # "waar" of "nietwaar"

        q = Weetje.query.get_or_404(question_ids[current_idx])
        current_answer = resp
        current_is_good = (resp == q.gender)
        answered_this_round = True
        current_idx += 1  # Alleen bij POST doorgaan

        return jsonify(status='ok')

    # GET: wordt gebruikt door frontend voor polling
    if current_idx == 0 or current_idx > len(question_ids):
        return jsonify(has_answer=False)

    q = Weetje.query.get(question_ids[current_idx - 1])  # Vorige vraag, want current_idx is al +1 gegaan
    return jsonify(
        has_answer=current_answer is not None,
        response=current_answer,
        is_good=current_is_good,
        uitleg=q.uitleg if q and q.uitleg else ""
    )


@Question_bp.route('/end')
def end():
    return render_template('Question/end.html')


@Question_bp.route('/health')
def health():
    return jsonify(status='ok')
