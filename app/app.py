#!/usr/bin/env python3
 
 
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
 
from models import db, Hero, Power, HeroPower
 
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False
 
CORS(app)
migrate = Migrate(app, db)
 
db.init_app(app)
 
 
@app.route("/heroes", methods=["GET"])
def get_heroes():
    # Query all heroes from the database
    heroes = Hero.query.all()
 
    # Format the data as a list of dictionaries
    heroes_data = [
        {"id": hero.id, "name": hero.name, "super_name": hero.super_name}
        for hero in heroes
    ]
 
    # Return the data as JSON
    return jsonify(heroes_data)
 
 
@app.route("/heroes/<int:id>", methods=["GET"])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if hero:
        hero_data = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [],
        }
        for hero_power in hero.hero_powers:
            power = hero_power.power
            power_data = {
                "id": power.id,
                "name": power.name,
                "description": power.description,
            }
            hero_data["powers"].append(power_data)
 
        return jsonify(hero_data)
    else:
        return make_response(jsonify({"error": "Hero not found"}), 404)
 
 
@app.route("/powers", methods=["GET"])
def get_powers():
    powers = Power.query.all()
    power_data = [
        {"id": power.id, "name": power.name, "description": power.description}
        for power in powers
    ]
    return jsonify(power_data)
 
 
@app.route("/powers/<int:id>", methods=["GET"])
def get_power(id):
    power = Power.query.get(id)
    if power:
        power_data = {
            "id": power.id,
            "name": power.name,
            "description": power.description,
        }
        return jsonify(power_data)
    else:
        response = {"error": "Power not found"}
        return jsonify(response), 404
 
 
@app.route("/powers/<int:id>", methods=["PATCH"])
def update_power(id):
    power = Power.query.get(id)
    if power:
        data = request.get_json()
        if "description" in data:
            power.description = data["description"]
        try:
            db.session.commit()
            power_data = {
                "id": power.id,
                "name": power.name,
                "description": power.description,
            }
            return jsonify(power_data)
        except Exception as e:
            db.session.rollback()
            response = {"errors": [str(e)]}
            return jsonify(response), 400
    else:
        response = {"error": "Power not found"}
        return jsonify(response), 404
 
 
@app.route("/hero_powers", methods=["POST"])
def create_hero_power():
    data = request.get_json()
    hero_id = data.get("hero_id")
    power_id = data.get("power_id")
    strength = data.get("strength")
 
    if not hero_id or not power_id or not strength:
        response = {"errors": ["Hero ID, Power ID, and Strength are required"]}
        return jsonify(response), 400
 
    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)
 
    if not hero or not power:
        response = {"errors": ["Hero or Power not found"]}
        return jsonify(response), 404
 
    try:
        # Attempt to create a new hero power
        hero_power = HeroPower(strength=strength, hero=hero, power=power)
        db.session.add(hero_power)
        db.session.commit()
 
        hero_data = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [
                {
                    "id": hero_power.power.id,
                    "name": hero_power.power.name,
                    "description": hero_power.power.description,
                }
            ],
        }
 
        return jsonify(hero_data)
 
    except ValueError as e:
        # Handle validation errors
        db.session.rollback()
        response = {"errors": [str(e)]}
        return jsonify(response), 400
 
    except Exception as e:
        # Handle other exceptions
        db.session.rollback()
        response = {"errors": [str(e)]}
        return jsonify(response), 500
 
 
if __name__ == "__main__":
    app.run(port=5555)