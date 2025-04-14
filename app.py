from flask import Flask, render_template
from flask_login import LoginManager, current_user
from datetime import datetime
from config.database import init_db
from models.user import User
from routes.auth import auth
from routes.admin import admin
from routes.cars import cars
from routes.insurance import insurance
from routes.comparisons import comparisons
from routes.chat import chat

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this in production!

# Initialize extensions
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Initialize database
init_db(app)

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(cars, url_prefix='/cars')
app.register_blueprint(insurance, url_prefix='/insurance')
app.register_blueprint(comparisons, url_prefix='/comparisons')
app.register_blueprint(chat, url_prefix='/chat')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.route('/')
def home():
    from models.car import Car
    from models.comparison import CarComparison
    
    # Get recent cars and comparisons if user is logged in
    recent_cars = []
    recent_comparisons = []
    
    if current_user.is_authenticated:
        recent_cars = Car.query.order_by(Car.created_at.desc()).limit(5).all()
        recent_comparisons = CarComparison.query.filter_by(user_id=current_user.id)\
            .order_by(CarComparison.created_at.desc()).limit(5).all()
    
    return render_template('index.html', 
                         recent_cars=recent_cars,
                         recent_comparisons=recent_comparisons)

if __name__ == '__main__':
    app.run(debug=True)
