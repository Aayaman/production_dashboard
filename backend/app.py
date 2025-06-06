from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, ProductionEntry
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)

@app.route("/")
def home():
    return "Flask backend running!"

@app.route("/api/entries", methods=["GET"])
def get_entries():
    entries = ProductionEntry.query.all()
    return jsonify([e.serialize() for e in entries])

@app.route("/api/entries", methods=["POST"])
def add_entry():
    try:
        data = request.get_json()
        print("Received JSON:", data)  # Debug log

        # Validate required fields
        if not all(k in data for k in ("station", "delay_reason", "duration")):
            return jsonify({"error": "Missing required fields"}), 400

        new_entry = ProductionEntry(
            station=data["station"],
            delay_reason=data["delay_reason"],
            duration=float(data["duration"])
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify(new_entry.serialize()), 201

    except Exception as e:
        print("Error during entry creation:", e)
        return jsonify({"error": str(e)}), 500

# Flask CLI command to create tables
@app.cli.command("create-db")
def create_db():
    db.create_all()
    print("Tables created successfully")

from routes import *

if __name__ == '__main__':
    app.run(debug=True)