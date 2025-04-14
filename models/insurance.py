from config.database import db


class InsuranceEstimate(db.Model):
    __tablename__ = 'insurance_estimates'

    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    coverage_type = db.Column(db.String(50), nullable=False)
    annual_premium = db.Column(db.Float, nullable=False)
    deductible = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Relationships
    car = db.relationship('Car', back_populates='insurance_estimates')
    user = db.relationship('User', back_populates='insurance_estimates')

    def __repr__(self):
        return f'<InsuranceEstimate {self.id} for Car {self.car_id}>'
