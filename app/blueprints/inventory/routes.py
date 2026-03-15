from flask import request, jsonify

from app.models import Inventory, Mechanics,db
from . import inventory_bp
from .schemas import inventory_schema,inventories_schema
from marshmallow import ValidationError
from sqlalchemy import select
from app.utils.util import token_required


##POST
@inventory_bp.route("/", methods=["POST"])
def add_part():
    try:
        part_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_part= Inventory(**part_data)
    db.session.add(new_part)
    db.session.commit()
    return inventory_schema.jsonify(new_part), 201


##GET ALl
@inventory_bp.route("/", methods=["GET"])
def get_parts():
    query = select(Inventory)
    parts = db.session.execute(query).scalars().all()

    return inventory_schema.jsonify(parts)


#Get one part
@inventory_bp.route("/<int:part_id>", methods=['GET'])
def get_part(part_id):
    part = db.session.get(Inventory, part_id)

    if part:
        return inventory_schema.jsonify(part), 200
    return jsonify({"error": "Part not found."}), 404


##PUT
@inventory_bp.route("/<int:part_id>", methods=["PUT"])
def update_part(part_id):
    part = db.session.get(Inventory, part_id)

    if not part:
        return jsonify({"error": "Part not found."}), 404
    
    try:
        part_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in part_data.items():
        setattr(part, key, value)

    db.session.commit()
    return inventory_schema.jsonify(part), 200


##DELETE
@inventory_bp.route("/<int:part_id>", methods=["DELETE"])
def delete_part(part_id):

    part = db.session.get(Inventory, part_id)

    if not part:
        return jsonify({"error": "Part not found."}), 404
    
    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": f'Part_id: {part_id}, successfully deleted.'}), 200