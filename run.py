from flask import Flask, render_template
from extensions import db, migrate, login_manager, mail, bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///indeling.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'zeer_geheime_sleutel'

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

mail.init_app(app)
bcrypt.init_app(app)

# Blueprints registreren
from routes.Behandeling.routes import Behandeling_bp
from routes.Beheerder.routes import Beheerder_bp
from routes.Weetje.routes import Weetje_bp
from routes.auth.routes import auth_bp

app.register_blueprint(Behandeling_bp, url_prefix='/Behandeling')
app.register_blueprint(Beheerder_bp, url_prefix='/Beheerder')
app.register_blueprint(Weetje_bp, url_prefix='/Weetje')
app.register_blueprint(auth_bp, url_prefix='/')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
