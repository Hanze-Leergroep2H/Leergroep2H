from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from models import Weetje

Question_bp = Blueprint('question', __name__, template_folder='templates')

# ─── Module‐level state (for single client only) ────────────────
question_ids = []
current_idx = 0
current_answer = None
current_is_good = None
answered_this_round = False
# ────────────────────────────────────────────────────────────────

@Question_bp.route('/start')
def start():
    global question_ids, current_idx, current_answer, current_is_good, answered_this_round
    question_ids = [w.id for w in Weetje.query.order_by(Weetje.id).all()]
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

    # Reset answer status for this round
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
            return jsonify(status='ignored')  # Prevent double-answering

        data = request.get_json()
        resp = data.get('response')  # "waar" or "nietwaar"

        q = Weetje.query.get_or_404(question_ids[current_idx])
        current_answer = resp
        current_is_good = (resp == q.gender)
        answered_this_round = True
        current_idx += 1  # Advance only on POST
        return jsonify(status='ok')

    # GET: used for polling to check if an answer is available
    return jsonify(
        has_answer=current_answer is not None,
        response=current_answer,
        is_good=current_is_good
    )

@Question_bp.route('/end')
def end():
    return render_template('Question/end.html')

@Question_bp.route('/health')
def health():
    return jsonify(status='ok')
