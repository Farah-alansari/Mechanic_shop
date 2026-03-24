
from flask import request, jsonify

from app.models import ServiceTickets, Mechanics,db
from . import tickets_bp
from .schemas import ticket_schema, tickets_schema, edit_ticket_schema
from marshmallow import ValidationError
from sqlalchemy import select
from app.utils.util import token_required



# CREATE TICKET
@tickets_bp.route("/", methods=["POST"])
@token_required
def create_ticket(current_customer_id):

    try:
        ticket_data = ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    ticket_data["customer_id"]= current_customer_id

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

@tickets_bp.route("/my-tickets", methods=["GET"])
@token_required
def get_my_tickets(customer_id):
    query = select(ServiceTickets).where(ServiceTickets.customer_id == customer_id)
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

@tickets_bp.route("/<int:ticket_id>", methods=["DELETE"])
def delete_ticket(ticket_id):

    ticket = db.session.get(ServiceTickets, ticket_id)

    if not ticket:
        return jsonify({"error": "Ticket not found."}), 404
    
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": f'ticket id: {ticket_id}, successfully deleted.'}), 200
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


@tickets_bp.route("/<int:ticket_id>", methods=["PUT"])
def edit_ticket(ticket_id):

    try:
        ticket_edits = edit_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(ServiceTickets).where(ServiceTickets.id == ticket_id)
    ticket = db.session.execute(query).scalars().first()

    # ADD MECHANICS
    for mech_id in ticket_edits["add_ids"]:
        query = select(Mechanics).where(Mechanics.id == mech_id)
        mechanic = db.session.execute(query).scalars().first()

        if mechanic and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)

    # REMOVE MECHANICS
    for mech_id in ticket_edits["remove_ids"]:
        query = select(Mechanics).where(Mechanics.id == mech_id)
        mechanic = db.session.execute(query).scalars().first()

        if mechanic and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)

    db.session.commit()

    return ticket_schema.jsonify(ticket)
