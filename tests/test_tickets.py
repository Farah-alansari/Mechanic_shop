
import unittest
from app import create_app
from app.models import db, Customers, ServiceTickets


class TestTickets(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')

        with self.app.app_context():
            db.drop_all()
            db.create_all()

           
            self.customer = Customers(
                name="test",
                email="test@email.com",
                phone="123456789",
                password="123"
            )

            db.session.add(self.customer)
            db.session.commit()

            self.client = self.app.test_client()

            login = self.client.post('/customers/login', json={
                "email": "test@email.com",
                "password": "123"
            })

          
            self.token = login.json["auth_token"]

            self.headers = {
                "Authorization": f"Bearer {self.token}"
            }

            ticket = ServiceTickets(
                vin="VIN123",
                service_date="2026-01-01",
                description="test issue",
                customer_id=self.customer.id
            )

            db.session.add(ticket)
            db.session.commit()
            self.ticket_id = ticket.id

 
    def test_create_ticket(self):
        payload = {
            "vin": "NEWVIN",
            "service_date": "2026-02-01",
            "description": "new issue",
            "customer_id": 1
        }

        response = self.client.post(
            "/tickets/",
            json=payload,
            headers=self.headers
        )
        print(response.json)
 
        self.assertEqual(response.status_code, 201)
  
    def test_invalid_ticket(self):
        payload = {
            "vin": "ONLYVIN"
        }

        response = self.client.post(
            "/tickets/",
            json=payload,
            headers=self.headers
        )

        self.assertEqual(response.status_code, 400)

 
    def test_get_tickets(self):
        response = self.client.get("/tickets/")

        self.assertEqual(response.status_code, 200)

    def test_get_my_tickets(self):
        response = self.client.get(
            "/tickets/my-tickets",
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200)

  
    def test_delete_ticket(self):
        response = self.client.delete(
            f"/tickets/{self.ticket_id}",
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200)
