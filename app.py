from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///superheroes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Hero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)
    hero_powers = db.relationship("HeroPower", backref="hero")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "super_name": self.super_name,
            "hero_powers": [hp.to_dict() for hp in self.hero_powers]
        }

    def to_dict_basic(self):
        return {
            "id": self.id,
            "name": self.name,
            "super_name": self.super_name
        }

class Power(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    hero_powers = db.relationship("HeroPower", backref="power")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

    def validate(self):
        errors = []
        if not self.description or len(self.description.strip()) < 20:
            errors.append("description must be at least 20 characters long")
        return errors

class HeroPower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey("hero.id", ondelete="CASCADE"), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey("power.id", ondelete="CASCADE"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "hero_id": self.hero_id,
            "power_id": self.power_id,
            "strength": self.strength,
            "power": self.power.to_dict() if self.power else None,
            "hero": self.hero.to_dict_basic() if self.hero else None
        }

    def validate(self):
        allowed = ["Strong", "Weak", "Average"]
        errors = []
        if self.strength not in allowed:
            errors.append("strength must be one of: Strong, Weak, Average")
        return errors

@app.route("/heroes", methods=["GET"])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([h.to_dict_basic() for h in heroes]), 200

@app.route("/heroes/<int:hero_id>", methods=["GET"])
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    return jsonify(hero.to_dict()), 200

@app.route("/powers", methods=["GET"])
def get_powers():
    powers = Power.query.all()
    return jsonify([p.to_dict() for p in powers]), 200

@app.route("/powers/<int:power_id>", methods=["GET"])
def get_power(power_id):
    power = Power.query.get(power_id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    return jsonify(power.to_dict()), 200

@app.route("/powers/<int:power_id>", methods=["PATCH"])
def patch_power(power_id):
    power = Power.query.get(power_id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    data = request.get_json()
    description = data.get("description")
    if description:
        power.description = description
    errors = power.validate()
    if errors:
        return jsonify({"errors": errors}), 400
    db.session.commit()
    return jsonify(power.to_dict()), 200

@app.route("/hero_powers", methods=["POST"])
def post_hero_power():
    data = request.get_json()
    strength = data.get("strength")
    hero_id = data.get("hero_id")
    power_id = data.get("power_id")
    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)
    hero_power = HeroPower(strength=strength, hero=hero, power=power)
    errors = hero_power.validate()
    if not hero or not power:
        errors.append("Hero or Power not found")
    if errors:
        return jsonify({"errors": errors}), 400
    db.session.add(hero_power)
    db.session.commit()
    return jsonify(hero_power.to_dict()), 201

if __name__ == "__main__":
    app.run(port=5555, debug=True)