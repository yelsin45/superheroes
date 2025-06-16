from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///superheroes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
migrate = Migrate(app, db)

@app.route("/heroes", methods=["GET"])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes]), 200

@app.route("/heroes/<int:id>", methods=["GET"])
def get_hero(id):
    hero = Hero.query.get_or_404(id)
    return jsonify(hero.to_dict(include_powers=True)), 200

@app.route("/powers", methods=["GET"])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers]), 200

@app.route("/powers/<int:id>", methods=["GET"])
def get_power(id):
    power = Power.query.get_or_404(id)
    return jsonify(power.to_dict()), 200

@app.route("/powers/<int:id>", methods=["PATCH"])
def patch_power(id):
    power = Power.query.get_or_404(id)
    data = request.get_json()
    description = data.get("description")
    if not description or len(description) < 20:
        return jsonify({"errors": ["Description must be at least 20 characters long"]}), 400
    power.description = description
    db.session.commit()
    return jsonify(power.to_dict()), 200

@app.route("/hero_powers", methods=["POST"])
def add_hero_power():
    data = request.get_json()
    strength = data.get("strength")
    power_id = data.get("power_id")
    hero_id = data.get("hero_id")
    if strength not in ["Strong", "Weak", "Average"]:
        return jsonify({"errors": ["Strength must be 'Strong', 'Weak', or 'Average'"]}), 400
    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)
    if not hero or not power:
        return jsonify({"errors": ["Hero or Power not found"]}), 400
    hero_power = HeroPower(strength=strength, hero_id=hero_id, power_id=power_id)
    db.session.add(hero_power)
    db.session.commit()
    return jsonify(hero.to_dict(include_powers=True)), 201

if __name__ == "__main__":
    app.run(port=5555, debug=True)