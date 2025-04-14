from datetime import datetime

from config.database import db


class CarComparison(db.Model):
    __tablename__ = 'car_comparisons'

    id = db.Column(db.Integer, primary_key=True)
    car1_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    car2_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Comparison results
    price_difference = db.Column(db.Float, nullable=False)
    conclusion = db.Column(db.Text)  # Summary of comparison
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Relationships
    car1 = db.relationship('Car', foreign_keys=[car1_id], back_populates='comparisons_as_car1')
    car2 = db.relationship('Car', foreign_keys=[car2_id], back_populates='comparisons_as_car2')
    user = db.relationship('User', back_populates='comparisons')

    def __repr__(self):
        return f'<CarComparison {self.car1.make} {self.car1.model} vs {self.car2.make} {self.car2.model}>'

    def to_dict(self):
        return {
            'id': self.id,
            'car1': self.car1.to_dict(),
            'car2': self.car2.to_dict(),
            'price_difference': self.price_difference,
            'conclusion': self.conclusion,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
