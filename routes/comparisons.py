from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required

from config.database import db
from models.car import Car
from models.comparison import CarComparison
from utils.mistral_ai import get_ai_response

comparisons = Blueprint('comparisons', __name__)

@comparisons.route('/')
@login_required
def list():
    page = request.args.get('page', 1, type=int)
    car_id = request.args.get('car_id', type=int)
    
    query = CarComparison.query.filter_by(user_id=current_user.id)
    if car_id:
        query = query.filter(
            (CarComparison.car1_id == car_id) |
            (CarComparison.car2_id == car_id)
        )
    
    pagination = query.order_by(CarComparison.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('comparisons/list.html',
                         comparisons=pagination.items,
                         pagination=pagination)

@comparisons.route('/generate', methods=['POST'])
@login_required
def generate():
    data = request.json
    car1 = data.get('car1')
    car2 = data.get('car2')
    price_difference = data.get('price_difference', 0)
    
    if not car1 or not car2:
        return jsonify({'error': 'Both cars are required'}), 400
    
    # Prepare the prompt for Mistral AI
    prompt = f"""Compare these two cars and provide a detailed analysis:

Car 1: {car1['year']} {car1['make']} {car1['model']}
Price: ${car1['price']:,.2f}
Description: {car1['description'] or 'No description available'}

Car 2: {car2['year']} {car2['make']} {car2['model']}
Price: ${car2['price']:,.2f}
Description: {car2['description'] or 'No description available'}

Price Difference: ${price_difference:,.2f}

Please provide a detailed comparison focusing on:
1. Value for money
2. Key differences in features and specifications
3. Target audience and use cases
4. Overall recommendation

Format the response in a clear, professional manner."""

    try:
        # Get AI response
        conclusion = get_ai_response([{"role": "user", "content": prompt}])
        return jsonify({'conclusion': conclusion})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@comparisons.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    car_id = request.args.get('car_id', type=int)
    car = Car.query.get_or_404(car_id) if car_id else None
    
    if request.method == 'POST':
        try:
            # Get the AI-generated conclusion from the form
            conclusion = request.form.get('conclusion', '')
            
            comparison = CarComparison(
                car1_id=request.form['car1_id'],
                car2_id=request.form['car2_id'],
                user_id=current_user.id,
                price_difference=float(request.form.get('price_difference', 0)),
                conclusion=conclusion
            )
            
            db.session.add(comparison)
            db.session.commit()
            flash('Comparison added successfully!', 'success')
            return redirect(url_for('comparisons.view', comparison_id=comparison.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding comparison: {str(e)}', 'error')
    
    # Get all cars and convert them to dictionaries
    cars = Car.query.all()
    cars_dict = [car.to_dict() for car in cars]
    
    return render_template('comparisons/form.html', 
                         car=car,
                         cars=cars_dict)

@comparisons.route('/<int:comparison_id>')
@login_required
def view(comparison_id):
    comparison = CarComparison.query.filter_by(id=comparison_id, user_id=current_user.id).first_or_404()
    return render_template('comparisons/view.html', comparison=comparison)

@comparisons.route('/<int:comparison_id>/delete', methods=['POST'])
@login_required
def delete(comparison_id):
    comparison = CarComparison.query.filter_by(id=comparison_id, user_id=current_user.id).first_or_404()
    try:
        db.session.delete(comparison)
        db.session.commit()
        flash('Comparison deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting comparison: {str(e)}', 'error')
    
    return redirect(url_for('comparisons.list'))
