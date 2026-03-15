from app.extensions import ma
from app.models import Customers


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customers


class LoginSchema(ma.Schema):
    email = ma.String(required= True)
    password = ma.String(required= True)
        
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
login_schema = LoginSchema()