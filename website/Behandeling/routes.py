from flask import Blueprint, render_template, redirect, url_for, flash
from models import db, Behandeling
from .form import BehandelingForm

Behandeling_bp = Blueprint('Behandeling', __name__, template_folder='templates')

@Behandeling_bp.route('/')
def index():
    Behandelingen = Behandeling.query.all()
    return render_template('Behandeling/index.html', Behandelingen=Behandelingen)

@Behandeling_bp.route('/add', methods=['GET', 'POST'])
def add():
    form = BehandelingForm()
    if form.validate_on_submit():
        Behandeling = Behandeling(plaats=form.plaats.data, soort=form.soort.data)
        db.session.add(Behandeling)
        db.session.commit()
        flash('Behandeling toegevoegd!', 'success')
        return redirect(url_for('Behandeling.index'))
    return render_template('Behandeling/form.html', form=form, title='Behandeling toevoegen')

@Behandeling_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    Behandeling = Behandeling.query.get_or_404(id)
    form = BehandelingForm(obj=Behandeling)
    if form.validate_on_submit():
        Behandeling.plaats = form.plaats.data
        Behandeling.soort = form.soort.data
        db.session.commit()
        flash('Behandeling bijgewerkt!', 'success')
        return redirect(url_for('Behandeling.index'))
    return render_template('Behandeling/form.html', form=form, title='Behandeling bewerken')

@Behandeling_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    Behandeling = Behandeling.query.get_or_404(id)
    db.session.delete(Behandeling)
    db.session.commit()
    flash('Behandeling verwijderd!', 'success')
    return redirect(url_for('Behandeling.index'))

@Behandeling_bp.route('/overzicht')
def overzicht():
    Behandelingen = Behandeling.query.options(db.joinedload(Behandeling.Weetje)).order_by(Behandeling.plaats).all()
    return render_template('overzicht.html', Behandelingen=Behandelingen, enumerate=enumerate)

