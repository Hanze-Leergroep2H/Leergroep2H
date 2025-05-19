from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from models import Beheerder
from extensions import db
from routes.Beheerder.form import BeheerderForm

Beheerder_bp = Blueprint('Beheerder', __name__, template_folder='templates')

@Beheerder_bp.route('/')
@login_required
def index():
    Beheerders = Beheerder.query.order_by(Beheerder.naam).all()
    return render_template('Beheerder/index.html', Beheerders=Beheerders)

@Beheerder_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = BeheerderForm()
    if form.validate_on_submit():
        WeetjeCreated = Beheerder(naam=form.naam.data, gender=form.gender.data)
        db.session.add(WeetjeCreated)
        db.session.commit()
        flash('Weetje toegevoegd!', 'success')
        return redirect(url_for('Beheerder.index'))
    return render_template('Beheerder/form.html', form=form, title='Beheerder toevoegen')

@Beheerder_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    Weetje1 = Beheerder.query.get_or_404(id)
    form = BeheerderForm(obj=Weetje1)
    if form.validate_on_submit():
        Weetje1.naam = form.naam.data
        Weetje1.gender = form.gender.data
        db.session.commit()
        flash('Weetje bijgewerkt!', 'success')
        return redirect(url_for('Beheerder.index'))
    return render_template('Beheerder/form.html', form=form, title='Beheerder bewerken')

@Beheerder_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    Weetje1 = Beheerder.query.get_or_404(id)
    db.session.delete(Weetje1)
    db.session.commit()
    flash('Beheerder verwijderd!', 'success')
    return redirect(url_for('Beheerder.index'))
