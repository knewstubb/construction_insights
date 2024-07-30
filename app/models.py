from app import db

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    highlights = db.Column(db.Text, nullable=False)
    lowlights = db.Column(db.Text, nullable=False)
    emerging_issues = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.String(19), nullable=False)  # '2024-07-30 15:26:39'
    weather = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Feedback('{self.timestamp}', '{self.weather}')"