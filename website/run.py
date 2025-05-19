from flask import Flask, render_template
from models import db
from Behandeling.routes import Behandeling_bp
from Weetje.routes import Weetje_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///indeling.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'zeer_geheime_sleutel'

db.init_app(app)

# Blueprints registreren
app.register_blueprint(Behandeling_bp, url_prefix='/Behandeling')
app.register_blueprint(Weetje_bp, url_prefix='/Weetje')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
