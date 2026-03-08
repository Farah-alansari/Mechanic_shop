
from flask import request, jsonify
from app.extensions import db
from app.models import ServiceTickets, Mechanics
from . import tickets_bp
from .schemas import ticket_schema, tickets_schema
from marshmallow import ValidationError
from sqlalchemy import select


# CREATE TICKET
@tickets_bp.route("/", methods=["POST"])
def create_ticket():

    try:
        ticket_data = ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_ticket = ServiceTickets(**ticket_data)

    db.session.add(new_ticket)
    db.session.commit()

    return ticket_schema.jsonify(new_ticket), 201


# GET 
@tickets_bp.route("/", methods=["GET"])
def get_tickets():

    query = select(ServiceTickets)
    tickets = db.session.execute(query).scalars().all()

    return tickets_schema.jsonify(tickets)


@tickets_bp.route("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=["PUT"])
def assign_mechanic(ticket_id, mechanic_id):

    ticket = db.session.get(ServiceTickets, ticket_id)
    mechanic = db.session.get(Mechanics, mechanic_id)

    if not ticket or not mechanic:
        return jsonify({"error": "Ticket or Mechanic not found"}), 404

    ticket.mechanics.append(mechanic)

    db.session.commit()

    return jsonify({"message": "Mechanic assigned successfully"}), 200


# REMOVE 
@tickets_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=["PUT"])
def remove_mechanic(ticket_id, mechanic_id):

    ticket = db.session.get(ServiceTickets, ticket_id)
    mechanic = db.session.get(Mechanics, mechanic_id)

    if not ticket or not mechanic:
        return jsonify({"error": "Ticket or Mechanic not found"}), 404

    ticket.mechanics.remove(mechanic)

    db.session.commit()

    return jsonify({"message": "Mechanic removed successfully"}), 200
