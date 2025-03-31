import openai  # Using OpenAI API to access Mistral AI
from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   url_for)
from flask_bcrypt import Bcrypt
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask App
app = Flask(__name__)

# Configurations
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' 

# Mistral AI API Key
openai.api_key = "your_mistral_api_key"

# User Loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Database Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    mileage = db.Column(db.Float, nullable=True)
    features = db.Column(db.Text, nullable=True)
    owner_history = db.Column(db.Text, nullable=True)
    accident_history = db.Column(db.Text, nullable=True)

class Insurance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    provider = db.Column(db.String(100), nullable=False)
    coverage_options = db.Column(db.Text, nullable=False)
    estimated_premium = db.Column(db.Float, nullable=False)
    past_claims = db.Column(db.Text, nullable=True)

# Routes
@app.route('/')
def home():
    cars = Car.query.all()
    return render_template('index.html', cars=cars)

# User Authentication
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Sprint 2: Car Management
@app.route('/cars/add', methods=['GET', 'POST'])
@login_required
def add_car():
    if request.method == 'POST':
        new_car = Car(
            brand=request.form['brand'],
            model=request.form['model'],
            year=request.form['year'],
            price=request.form['price'],
            mileage=request.form['mileage'],
            features=request.form['features'],
            owner_history=request.form['owner_history'],
            accident_history=request.form['accident_history']
        )
        db.session.add(new_car)
        db.session.commit()
        flash('Car added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_car.html')

@app.route('/cars/delete/<int:car_id>')
@login_required
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    flash('Car deleted successfully!', 'danger')
    return redirect(url_for('home'))

# Sprint 2: Insurance Management
@app.route('/insurance/add', methods=['GET', 'POST'])
@login_required
def add_insurance():
    if request.method == 'POST':
        new_insurance = Insurance(
            car_id=request.form['car_id'],
            provider=request.form['provider'],
            coverage_options=request.form['coverage_options'],
            estimated_premium=request.form['estimated_premium'],
            past_claims=request.form['past_claims']
        )
        db.session.add(new_insurance)
        db.session.commit()
        flash('Insurance added successfully!', 'success')
        return redirect(url_for('home'))
    cars = Car.query.all()
    return render_template('add_insurance.html', cars=cars)

# Sprint 3: AI-Powered Car Comparison
@app.route('/compare', methods=['GET', 'POST'])
@login_required
def compare():
    cars = Car.query.all()
    if request.method == 'POST':
        car1 = Car.query.get(request.form['car1'])
        car2 = Car.query.get(request.form['car2'])

        # Prepare input for AI
        prompt = f"""
        Compare these two cars based on price, mileage, features, and overall value:
        Car 1: {car1.brand} {car1.model} ({car1.year})
        - Price: ${car1.price}
        - Mileage: {car1.mileage} miles
        - Features: {car1.features}
        - Accident History: {car1.accident_history}

        Car 2: {car2.brand} {car2.model} ({car2.year})
        - Price: ${car2.price}
        - Mileage: {car2.mileage} miles
        - Features: {car2.features}
        - Accident History: {car2.accident_history}

        Provide a detailed, unbiased comparison highlighting the pros and cons of both cars.
        """

        # Call Mistral AI
        response = openai.ChatCompletion.create(
            model="mistral-7b-instruct",  
            messages=[{"role": "user", "content": prompt}]
        )
        
        comparison_result = response["choices"][0]["message"]["content"]
        return render_template('compare_result.html', car1=car1, car2=car2, result=comparison_result)

    return render_template('compare.html', cars=cars)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
