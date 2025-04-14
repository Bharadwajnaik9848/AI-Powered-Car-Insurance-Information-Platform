from flask import Blueprint, render_template, redirect, url_for, flash, request
from routes.auth import admin_required
from models.car import Car
from models.insurance import InsuranceEstimate
from models.user import User
from config.database import db

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/')
@admin_required
def dashboard():
    stats = {
        'total_users': User.query.count(),
        'total_cars': Car.query.count(),
        'total_insurance_estimates': InsuranceEstimate.query.count(),
        'recent_users': User.query.order_by(User.created_at.desc()).limit(5).all(),
        'recent_cars': Car.query.order_by(Car.created_at.desc()).limit(5).all(),
        'recent_estimates': InsuranceEstimate.query.order_by(InsuranceEstimate.created_at.desc()).limit(5).all()
    }
    return render_template('admin/dashboard.html', stats=stats)

@admin.route('/users')
@admin_required
def users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@admin.route('/users/<int:user_id>/toggle-admin', methods=['POST'])
@admin_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        flash('Cannot modify your own admin status', 'error')
    else:
        user.is_admin = not user.is_admin
        db.session.commit()
        flash(f'Admin status updated for {user.username}', 'success')
    return redirect(url_for('admin.users'))

@admin.route('/cars')
@admin_required
def cars():
    cars = Car.query.order_by(Car.created_at.desc()).all()
    return render_template('admin/cars.html', cars=cars)

@admin.route('/cars/add', methods=['GET', 'POST'])
@admin_required
def add_car():
    if request.method == 'POST':
        car = Car(
            make=request.form.get('make'),
            model=request.form.get('model'),
            year=int(request.form.get('year')),
            category=request.form.get('category'),
            fuel_type=request.form.get('fuel_type'),
            price=float(request.form.get('price')),
            created_by_id=current_user.id
        )
        db.session.add(car)
        db.session.commit()
        flash('Car added successfully', 'success')
        return redirect(url_for('admin.cars'))
    return render_template('admin/car_form.html')

@admin.route('/cars/<int:car_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_car(car_id):
    car = Car.query.get_or_404(car_id)
    if request.method == 'POST':
        car.make = request.form.get('make')
        car.model = request.form.get('model')
        car.year = int(request.form.get('year'))
        car.category = request.form.get('category')
        car.fuel_type = request.form.get('fuel_type')
        car.price = float(request.form.get('price'))
        db.session.commit()
        flash('Car updated successfully', 'success')
        return redirect(url_for('admin.cars'))
    return render_template('admin/car_form.html', car=car)

@admin.route('/cars/<int:car_id>/delete', methods=['POST'])
@admin_required
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    flash('Car deleted successfully', 'success')
    return redirect(url_for('admin.cars'))

@admin.route('/insurance')
@admin_required
def insurance():
    estimates = InsuranceEstimate.query.order_by(InsuranceEstimate.created_at.desc()).all()
    return render_template('admin/insurance.html', estimates=estimates)

@admin.route('/insurance/<int:estimate_id>/delete', methods=['POST'])
@admin_required
def delete_insurance(estimate_id):
    estimate = InsuranceEstimate.query.get_or_404(estimate_id)
    db.session.delete(estimate)
    db.session.commit()
    flash('Insurance estimate deleted successfully', 'success')
    return redirect(url_for('admin.insurance'))
