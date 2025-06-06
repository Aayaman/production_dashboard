from app import app, db
from flask import request, jsonify, render_template
from models import ProductionEntry


@app.route('/api/data', methods=['GET'])
def get_data_route():
    entries = ProductionEntry.query.order_by(ProductionEntry.timestamp.desc()).all()
    return jsonify([e.serialize() for e in entries])

@app.route('/api/add', methods=['POST'])
def add_entry_route():
    data = request.json
    try:
        new_entry = ProductionEntry(
            station=data['station'],
            delay_reason=data['delay_reason'],
            duration=float(data['duration'])
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"message": "Entry added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
