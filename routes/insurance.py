from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from config.database import db
from models.car import Car
from models.insurance import InsuranceEstimate

insurance = Blueprint('insurance', __name__)

@insurance.route('/')
@login_required
def estimates():
    page = request.args.get('page', 1, type=int)
    car_id = request.args.get('car_id', type=int)
    
    query = InsuranceEstimate.query.filter_by(user_id=current_user.id)
    if car_id:
        query = query.filter_by(car_id=car_id)
    
    pagination = query.order_by(InsuranceEstimate.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('insurance/list.html', 
                         estimates=pagination.items, 
                         pagination=pagination)

@insurance.route('/add', methods=['GET', 'POST'])
@login_required
def add_estimate():
    car_id = request.args.get('car_id', type=int)
    car = Car.query.get_or_404(car_id) if car_id else None
    
    if request.method == 'POST':
        try:
            estimate = InsuranceEstimate(
                car_id=request.form['car_id'],
                user_id=current_user.id,
                coverage_type=request.form['coverage_type'],
                annual_premium=float(request.form['annual_premium']),
                deductible=float(request.form['deductible'])
            )
            
            db.session.add(estimate)
            db.session.commit()
            flash('Insurance estimate added successfully!', 'success')
            return redirect(url_for('insurance.view_estimate', estimate_id=estimate.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding insurance estimate: {str(e)}', 'error')
    
    cars = Car.query.all()
    return render_template('insurance/form.html', car=car, cars=cars)

@insurance.route('/<int:estimate_id>')
@login_required
def view_estimate(estimate_id):
    estimate = InsuranceEstimate.query.filter_by(id=estimate_id, user_id=current_user.id).first_or_404()
    return render_template('insurance/view.html', estimate=estimate)

@insurance.route('/<int:estimate_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_estimate(estimate_id):
    estimate = InsuranceEstimate.query.filter_by(id=estimate_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        try:
            estimate.coverage_type = request.form['coverage_type']
            estimate.annual_premium = float(request.form['annual_premium'])
            estimate.deductible = float(request.form['deductible'])
            
            db.session.commit()
            flash('Insurance estimate updated successfully!', 'success')
            return redirect(url_for('insurance.view_estimate', estimate_id=estimate.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating insurance estimate: {str(e)}', 'error')
    
    return render_template('insurance/form.html', estimate=estimate)

@insurance.route('/<int:estimate_id>/delete', methods=['POST'])
@login_required
def delete_estimate(estimate_id):
    estimate = InsuranceEstimate.query.filter_by(id=estimate_id, user_id=current_user.id).first_or_404()
    try:
        db.session.delete(estimate)
        db.session.commit()
        flash('Insurance estimate deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting insurance estimate: {str(e)}', 'error')
    
    return redirect(url_for('insurance.estimates'))
