Superheroes Flask API

A simple RESTful API for managing superheroes and their powers, built with Flask, SQLAlchemy, and Flask-Migrate.



 Features

- List superheroes and their powers
- Add, update, and view heroes and powers
- Assign powers to heroes with different strengths
- Many-to-many relationship (HeroPower) between heroes and powers

Database Structure

- heroes: id, name, super_name  
- powers: id, name, description  
- hero_powers: id, strength, hero_id, power_id (join table)

Getting Started

 Install dependencies (using pipenv)

bash
pipenv install
pipenv shell

 Run migrations

bash
flask db init         # First time only
flask db migrate -m "Initial migration"
flask db upgrade

 Seed the database
python seed.py

 Run the server


flask run --port=5555

 API Endpoints

| Method | Route                  | Description                      |
|--------|------------------------|----------------------------------|
| GET    | /heroes                | List all heroes                  |
| GET    | /heroes/&lt;id&gt;     | Get a hero & their powers        |
| GET    | /powers                | List all powers                  |
| GET    | /powers/&lt;id&gt;     | Get a power                      |
| PATCH  | /powers/&lt;id&gt;     | Update a power's description     |
| POST   | /hero_powers           | Add a power to a hero            |

