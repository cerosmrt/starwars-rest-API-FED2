"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite

def get_current_user():
    user = User.query.first()
    if not user:
        raise Exception("No current user found")
    return user

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    all_people = list(map(lambda x: x.serialize(), people))
    
    return jsonify(all_people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people(people_id):
    people = People.query.get(people_id)
    if people is None:
        return "No People with id: " + str(people_id), 400
    
    one_people = people.serialize()
    
    return jsonify(one_people), 200

@app.route('/people', methods=['POST'])
def create_people():
        
    new_people = request.get_json()

    if 'name' not in new_people:
        return "Name should be in New People Body", 400
    
    new_people = People(
        name = new_people['name'],
        age = new_people['age'],
        gender = new_people['gender']
                        )
    db.session.add(new_people)
    db.session.commit()
    
    return jsonify({"msg": "New People is Created"}), 201

@app.route('/people/<int:people_id>', methods=['PUT'])
def update_people(people_id):
        
    new_updated_people = request.get_json()
    old_people_obj = People.query.get(people_id)

    if old_people_obj is None:
        return "No People with id: " + str(people_id), 400

    if 'name' in new_updated_people:
        old_people_obj.name = new_updated_people['name']

    if 'age' in new_updated_people: 
        old_people_obj.age = new_updated_people['age']

    if 'gender' in new_updated_people:
        old_people_obj.gender  = new_updated_people['gender']   

    db.session.commit()
    
    return jsonify({"msg": "People is Updated"}), 200

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_people(people_id):
        
    deleting_people = People.query.get(people_id)

    if deleting_people is None:
        return "No People with id: " + str(people_id), 400

    db.session.delete(deleting_people)
    db.session.commit()
    
    return jsonify({"msg": "People is Deleted"}), 200

@app.route('/planets', methods=['POST'])
def create_planet():
    new_planet = request.get_json()

    if 'name' not in new_planet:
        return "Name should be in New Planet Body", 400
    
    new_planet = Planet(
        name = new_planet['name'],
        size = new_planet['size'],
        population = new_planet['population']
    )
    db.session.add(new_planet)
    db.session.commit()
    
    return jsonify({"msg": "New Planet is Created"}), 201

@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    new_updated_planet = request.get_json()
    old_planet_obj = Planet.query.get(planet_id)

    if old_planet_obj is None:
        return "No Planet with id: " + str(planet_id), 400

    if 'name' in new_updated_planet:
        old_planet_obj.name = new_updated_planet['name']

    if 'size' in new_updated_planet: 
        old_planet_obj.size = new_updated_planet['size']

    if 'population' in new_updated_planet:
        old_planet_obj.population  = new_updated_planet['population']   

    db.session.commit()
    
    return jsonify({"msg": "Planet is Updated"}), 200

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    deleting_planet = Planet.query.get(planet_id)

    if deleting_planet is None:
        return "No Planet with id: " + str(planet_id), 400

    db.session.delete(deleting_planet)
    db.session.commit()
    
    return jsonify({"msg": "Planet is Deleted"}), 200

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))
    return jsonify(all_users), 200

@app.route('/users', methods=['POST'])
def create_user():
    new_user = request.get_json()

    if 'username' not in new_user:
        return "Username should be in New User Body", 400
    
    new_user = User(
        username = new_user['username'],
        email = new_user['email'],
        password = new_user['password']
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"msg": "New User is Created"}), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    new_updated_user = request.get_json()
    old_user_obj = User.query.get(user_id)

    if old_user_obj is None:
        return "No User with id: " + str(user_id), 400

    if 'username' in new_updated_user:
        old_user_obj.username = new_updated_user['username']

    if 'email' in new_updated_user: 
        old_user_obj.email = new_updated_user['email']

    if 'password' in new_updated_user:
        old_user_obj.password  = new_updated_user['password']   

    db.session.commit()
    
    return jsonify({"msg": "User is Updated"}), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    deleting_user = User.query.get(user_id)

    if deleting_user is None:
        return "No User with id: " + str(user_id), 400

    db.session.delete(deleting_user)
    db.session.commit()
    
    return jsonify({"msg": "User is Deleted"}), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user = get_current_user()
    favorites = list(map(lambda x: x.serialize(), user.favorites))
    return jsonify(favorites), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user = get_current_user()
    planet = Planet.query.get(planet_id)
    if planet is None:
        return "No Planet with id: " + str(planet_id), 404
    favorite = Favorite(user=user, planet=planet)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user = get_current_user()
    people = People.query.get(people_id)
    if people is None:
        return "No People with id: " + str(people_id), 404
    favorite = Favorite(user=user, people=people)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user = get_current_user()
    favorite = Favorite.query.filter_by(user=user, planet_id=planet_id).first()
    if favorite is None:
        return "No favorite Planet with id: " + str(planet_id), 404
    db.session.delete(favorite)
    db.session.commit()
    return '', 204

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user = get_current_user()
    favorite = Favorite.query.filter_by(user=user, people_id=people_id).first()
    if favorite is None:
        return "No favorite People with id: " + str(people_id), 404
    db.session.delete(favorite)
    db.session.commit()
    return '', 204

# Add the other endpoints as necessary

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
