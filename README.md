# Mechanics Shop API

## Description

This project is a RESTful API built using Flask for managing a mechanics shop system. It supports CRUD operations for Inventory, Customers, Mechanics, and Tickets. Swagger UI is included for API documentation and testing.

## Setup Instructions

1. Clone the repository:
   git clone <your-repo-url>
   cd mechanics_shop

2. Create virtual environment:
   python -m venv venv

3. Activate virtual environment:
   Windows: venv\Scripts\activate
   Mac/Linux: source venv/bin/activate

4. Install dependencies:
   pip install -r requirements.txt

## Run the Application

python app.py
API runs on http://127.0.0.1:5000
Swagger docs: http://127.0.0.1:5000/api/docs

## Running Tests

python -m unittest discover tests

## Features

- CRUD operations
- Swagger documentation
- Unit testing
- Negative test cases

## Author

Farah Alansari
