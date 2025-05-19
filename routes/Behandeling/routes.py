from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from extensions import db
from models import Behandeling, Beheerder
from .form import BehandelingForm

Behandeling_bp = Blueprint('Behandeling', __name__, template_folder='templates')

@Behandeling_bp.route('/')
@login_required
def index():
    Behandelingen = Behandeling.query.all()
    return render_template('Behandeling/index.html', Behandelingen=Behandelingen)

@Behandeling_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = BehandelingForm()
    if form.validate_on_submit():
        nieuwe_behandeling = Behandeling(behandelingnaam=form.behandelingnaam.data, Categorie=form.Categorie.data, Beheerder_id=form.Beheerder_id.data)
        db.session.add(nieuwe_behandeling)
        db.session.commit()
        flash('Behandeling toegevoegd!', 'success')
        return redirect(url_for('Behandeling.index'))
    return render_template('Behandeling/form.html', form=form, title='Behandeling toevoegen')

@Behandeling_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    Behandeling = Behandeling.query.get_or_404(id)
    form = BehandelingForm(obj=Behandeling)
    if form.validate_on_submit():
        Behandeling.behandelingnaam = form.behandelingnaam.data
        Behandeling.Categorie = form.Categorie.data
        Behandeling.Beheerder.id=form.Beheerder_id.data
        db.session.commit()
        flash('Behandeling bijgewerkt!', 'success')
        return redirect(url_for('Behandeling.index'))
    return render_template('Behandeling/form.html', form=form, title='Behandeling bewerken')

@Behandeling_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    nieuwe_behandeling = Behandeling.query.get_or_404(id)
    db.session.delete(nieuwe_behandeling)
    db.session.commit()
    flash('Behandeling verwijderd!', 'success')
    return redirect(url_for('Behandeling.index'))

@Behandeling_bp.route('/overzicht')
def overzicht():
    Behandelingen = Behandeling.query.options(
        db.joinedload(Behandeling.Weetje),
        db.joinedload(Behandeling.Beheerder)  
    ).order_by(Behandeling.behandelingnaam).all()
    return render_template('overzicht.html', Behandelingen=Behandelingen, enumerate=enumerate)
