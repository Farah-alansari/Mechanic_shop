from app.extensions import ma
from app.models import ServiceTickets
from marshmallow import fields




class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTickets
        include_fk= True
       
class EditTicketSchema(ma.Schema):
    add_ids= fields.List(fields.Int(), required= True)
    remove_ids = fields.List(fields.Int(), required=True)
    
    class Meta:
        fields=("add_ids", "remove_ids")

ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)
edit_ticket_schema = EditTicketSchema()

