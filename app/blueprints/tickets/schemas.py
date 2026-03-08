from app.extensions import ma
from app.models import ServiceTickets



class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTickets
        include_fk= True
       


ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)