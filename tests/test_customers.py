from app import create_app
from app.models import db, Customers
import unittest


class TestCustomers(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.customer = Customers(
            name="test_user", 
            email="test@email.com", 
            phone="123456789",
            password="123")
        
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
            db.session.refresh(self.customer)
            self.client = self.app.test_client()

# create
    def test_create_customer(self):
        customer_payload = {
            "name": "Farah",
            "email": "farah@email.com",
            "phone":"88888888",
            "password": "123"
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Farah")
    
    
    #invalid
    def test_invalid_creation(self):
        customer_payload = {
           "name": "Farah",
            "phone":"88888888",
            "password": "123"
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field.'])

    #login
    def test_login_customer(self):
        credentials = {
            "email": "test@email.com",
            "password": "123"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        token = response.json['auth_token']
    
    #invalid login
    def test_invalid_login(self):
        credentials = {
            "email": "wrong@email.com",
            "password": "wrong_pw"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['messages'], 'Invalid email')
     
    #get all
    def test_get_all_customers(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        
    
    #put
    
    def test_update_customer(self):
        customer_payload={
            "name": "Updated Name",
            "email": "updatedh@email.com",
            "phone":"111111111",
            "password": "123"
        }

        response = self.client.put(f'/customers/{self.customer.id}',
        json = customer_payload
    )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Updated Name")

    #delete
    def test_delete_customers(self):
        response = self.client.delete (f'/customers/{self.customer.id}')
        self.assertEqual(response.status_code, 200)