from config.database import db


class Car(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='cars')
    insurance_estimates = db.relationship('InsuranceEstimate', back_populates='car')
    comparisons_as_car1 = db.relationship('CarComparison', 
                                        foreign_keys='CarComparison.car1_id',
                                        back_populates='car1')
    comparisons_as_car2 = db.relationship('CarComparison', 
                                        foreign_keys='CarComparison.car2_id',
                                        back_populates='car2')

    def __repr__(self):
        return f'<Car {self.year} {self.make} {self.model}>'

    def to_dict(self):
        return {
            'id': self.id,
            'make': self.make,
            'model': self.model,
            'year': self.year,
            'price': self.price,
            'description': self.description
        }
