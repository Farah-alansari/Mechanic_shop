from app import create_app
from app.models import db, Mechanics
import unittest


class TestMechanics(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.mechanic = Mechanics(
            name="test_mechanic", 
            email="mech@email.com", 
            phone="123456789",
            salary=3000)
        
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
            db.session.refresh(self.mechanic)
            self.client = self.app.test_client()

# create
    def test_create_mechanic(self):
        mechanic_payload = {
            "name": "Fadi",
            "email": "fadi@email.com",
            "phone":"666666666",
            "salary": 4000
        }

        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Fadi")
    
    
    #invalid
    def test_invalid_creation(self):
        mechanic_payload = {
            "name": "Fadi",
        }

        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 400)
   
    #get 
    def test_get_mechanic(self):
        response = self.client.get(f'/mechanics/{self.mechanic.id}')
        self.assertEqual(response.status_code, 200)
    #get all
    def test_get_all_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        
    
    #put
    
    def test_update_mechanic(self):
        mechanic_payload={
            "name": "Updated_name",
            "email": "updated@email.com",
            "phone":"111111111",
            "salary": 5000
        }

        response = self.client.put(f'/mechanics/{self.mechanic.id}',
        json = mechanic_payload
    )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Updated_name")

    #delete
    def test_delete_mechanics(self):
        response = self.client.delete (f'/mechanics/{self.mechanic.id}')
        self.assertEqual(response.status_code, 200)
        
    #popualr
    def test_popualr_mechanic(self):
        response = self.client.get (f'/mechanics/popular')
        self.assertEqual(response.status_code, 200)
        
    
      #serach
    def test_search_mechanic(self):
        response = self.client.get (f'/mechanics/search')
        self.assertEqual(response.status_code, 200)
        