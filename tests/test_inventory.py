import unittest
from app import create_app
from app.models import db, Inventory

class TestInventory(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            # create sample part
            part = Inventory(
                name="Engine Oil",
                price=50.0
            )

            db.session.add(part)
            db.session.commit()
            db.session.refresh(part)
            self.part_id =part.id

        self.client = self.app.test_client()

    # CREATE
    def test_create_part(self):
        payload = {
            "name": "Brake Pads",
            "price": 120.0
        }

        response = self.client.post("/inventory/", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "Brake Pads")

    # INVALID
    def test_invalid_part(self):
        payload = {
            "name": "OnlyName"
        }

        response = self.client.post("/inventory/", json=payload)
        self.assertEqual(response.status_code, 400)

    # GET ALL
    def test_get_all_parts(self):
        payload={
            "name": "Brake Pad",
            "price": 50
        }
        
        self.client.post('/inventory/', json=payload)
       
        response =self.client.get("/inventory/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) > 0)

    # GET ONE
    def test_get_part(self):
        response = self.client.get(f"/inventory/{self.part_id}")
        self.assertEqual(response.status_code, 200)

    # UPDATE
    def test_update_part(self):
        payload = {
            "name": "Updated Part",
            "price": 200.0
        }

        response = self.client.put(f"/inventory/{self.part_id}", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Updated Part")

    # DELETE
    def test_delete_part(self):
        response = self.client.delete(f"/inventory/{self.part_id}")
        self.assertEqual(response.status_code, 200)
