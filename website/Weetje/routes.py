from flask import Blueprint, render_template, redirect, url_for, flash
from models import db, Weetje
from .form import WeetjeForm

Weetje_bp = Blueprint('Weetje', __name__, template_folder='templates')

@Weetje_bp.route('/')
def index():
    Weetjes = Weetje.query.order_by(Weetje.Weetje).all()
    return render_template('Weetje/index.html', Weetjes=Weetjes)

@Weetje_bp.route('/add', methods=['GET', 'POST'])
def add():
    form = WeetjeForm()
    if form.validate_on_submit():
        # Behandeling = Behandeling.query.get(form.Behandeling_id.data)
        WeetjeCreated = Weetje(Weetje=form.Weetje.data, gender=form.gender.data, Behandeling_id=form.Behandeling_id.data)
        db.session.add(WeetjeCreated)
        db.session.commit()
        flash('Weetje toegevoegd!', 'success')
        return redirect(url_for('Weetje.index'))
    return render_template('Weetje/form.html', form=form, title='Weetje toevoegen')

@Weetje_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    Weetje1 = Weetje.query.get_or_404(id)
    form = WeetjeForm(obj=Weetje1)
    if form.validate_on_submit():
        Weetje1.Weetje = form.Weetje.data
        Weetje1.gender = form.gender.data
        Weetje1.Behandeling_id = form.Behandeling_id.data
        db.session.commit()
        flash('Weetje bijgewerkt!', 'success')
        return redirect(url_for('Weetje.index'))
    return render_template('Weetje/form.html', form=form, title='Weetje bewerken')

@Weetje_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    Weetje = Weetje.query.get_or_404(id)
    db.session.delete(Weetje)
    db.session.commit()
    flash('Weetje verwijderd!', 'success')
    return redirect(url_for('Weetje.index'))
