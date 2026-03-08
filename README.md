Mechanics Shop API

# About the Project

This project is a Flask REST API for a mechanic shop. It manages mechanics, customers, and service tickets. The API allows creating tickets and assigning or removing mechanics.

# Technologies

• Python
• Flask
• SQLAlchemy
• Marshmallow
• Postman

# Main Endpoints

• POST /mechanics – create mechanic
• GET /mechanics – get all mechanics
• PUT /mechanics/<id> – update mechanic
• DELETE /mechanics/<id> – delete mechanic
• POST /tickets – create ticket
• GET /tickets – get all tickets
• PUT /tickets/<ticket_id>/assign-mechanic/<mechanic_id>
• PUT /tickets/<ticket_id>/remove-mechanic/<mechanic_id>

# Testing

All endpoints were tested using Postman.

## Author

Farah Al-Ansari
