from flask import request, jsonify
from app.extensions import limiter,cache
from app.models import Mechanics,db
from . import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema
from marshmallow import ValidationError
from sqlalchemy import select

##POST
@mechanics_bp.route("/", methods=["POST"])
## Rate limiting to prevent too many mechanics creations in a short time
@limiter.limit("3 per hour")
def add_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Mechanics).where(Mechanics.email == mechanic_data['email']) 
    existing_mechanic = db.session.execute(query).scalars().all()
    if existing_mechanic:
        return jsonify({"error": "Email already associated with a mechanic."}), 400
    
    new_mechanic = Mechanics(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201


##GET
@mechanics_bp.route("/", methods=["GET"])
## reduce database load
@cache.cached(timeout=60)
def get_mechanics():
    query = select(Mechanics)
    mechanics = db.session.execute(query).scalars().all()

    return mechanic_schema.jsonify(mechanics)

@mechanics_bp.route("/<int:mechanic_id>", methods=['GET'])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)

    if mechanic:
        return mechanic_schema.jsonify(mechanic), 200
    return jsonify({"error": "Mechanic not found."}), 404

##PUT

@mechanics_bp.route("/<int:mechanic_id>", methods=["PUT"])
def update_mechanics(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)

    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


##DELETE
@mechanics_bp.route("/<int:mechanic_id>", methods=["DELETE"])
def delete_mechanic(mechanic_id):

    mechanic = db.session.get(Mechanics, mechanic_id)

    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f'Mechanic id: {mechanic_id}, successfully deleted.'}), 200

@mechanics_bp.route("/popular", methods=["Get"])
def popular_mechanics():
    query= select(Mechanics)
    mechanics= db.session.execute(query).scalars().all()
    mechanics.sort(key=lambda mechanic: len(mechanic.tickets), reverse=True)
    return mechanics_schema.jsonify(mechanics)

@mechanics_bp.route("/search", methods=['GET'])
def search_mechanic():
    name = request.args.get("name")
    
    query = select(Mechanics).where(Mechanics.name.like(f'%{name}%')) 
    mechanics = db.session.execute(query).scalars().all()

    return mechanics_schema.jsonify(mechanics)