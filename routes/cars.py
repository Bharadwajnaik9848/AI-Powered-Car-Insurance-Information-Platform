from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user

from config.database import db
from models.car import Car

cars = Blueprint('cars', __name__)

@cars.route('/cars')
def list_cars():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Car.query
    
    if search:
        query = query.filter(
            (Car.make.ilike(f'%{search}%')) |
            (Car.model.ilike(f'%{search}%'))
        )
    
    pagination = query.order_by(Car.created_at.desc()).paginate(
        page=page, per_page=9, error_out=False
    )
    
    return render_template('cars/list.html', cars=pagination.items, pagination=pagination)

@cars.route('/cars/add', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        try:
            car = Car(
                make=request.form['make'],
                model=request.form['model'],
                year=int(request.form['year']),
                price=float(request.form['price']),
                description=request.form.get('description', ''),
                user_id=current_user.id
            )
            db.session.add(car)
            db.session.commit()
            flash('Car added successfully!', 'success')
            return redirect(url_for('cars.view_car', car_id=car.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding car: {str(e)}', 'error')
    
    return render_template('cars/form.html')

@cars.route('/cars/<int:car_id>')
def view_car(car_id):
    car = Car.query.get_or_404(car_id)
    return render_template('cars/view.html', car=car)

@cars.route('/cars/<int:car_id>/edit', methods=['GET', 'POST'])
def edit_car(car_id):
    car = Car.query.get_or_404(car_id)
    
    if request.method == 'POST':
        try:
            car.make = request.form['make']
            car.model = request.form['model']
            car.year = int(request.form['year'])
            car.price = float(request.form['price'])
            car.description = request.form.get('description', '')
            
            db.session.commit()
            flash('Car updated successfully!', 'success')
            return redirect(url_for('cars.view_car', car_id=car.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating car: {str(e)}', 'error')
    
    return render_template('cars/form.html', car=car)

@cars.route('/cars/<int:car_id>/delete', methods=['POST'])
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    try:
        db.session.delete(car)
        db.session.commit()
        flash('Car deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting car: {str(e)}', 'error')
    
    return redirect(url_for('cars.list_cars'))
