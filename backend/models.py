from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class ProductionEntry(db.Model):
    __tablename__ = 'production_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    station = db.Column(db.String(50), nullable=False)
    delay_reason = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Float, nullable=False)  # in minutes

    def serialize(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "station": self.station,
            "delay_reason": self.delay_reason,
            "duration": self.duration
        }
