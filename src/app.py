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
from models import db, User,Planeta,Personaje,Favoritos
#from models import Person
CURRENT_USER_ID=1

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

@app.route('/planetas', methods=['GET'])
def get_all_planets():
    planetas = Planeta.query.all()
    result = [planeta.serialize() for planeta in planetas]
    return jsonify({"result":result}),200


@app.route('/planeta/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planeta = Planeta.query.get(planet_id)
    if planeta is None:
        return jsonify({" mensage: no existe 404"}),404
    return jsonify(planeta.serialize()),200

@app.route('/personajes', methods=['GET'])
def get_all_people():
    personajes = Personaje.query.all()
    result = [personaje.serialize() for personaje in personajes]
    return jsonify({"result":result}),200


@app.route('/personaje/<int:personaje_id>', methods=['GET'])
def get_person(personaje_id):
    personaje = Personaje.query.get(personaje_id)
    if personaje is None:
        return jsonify({" mensage: no existe 404"}),404
    return jsonify(personaje.serialize()),200

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    result = [user.serialize() for user in users]
    return jsonify({"result":result}),200

@app.route('/users/favorites', methods=['GET'])
def get_user_favoritos():
    favoritos = Favoritos.query.filter_by(user_id=CURRENT_USER_ID).all()
    # favoritos_lista = [{"id": fav.id, "planet": fav.planet.name if fav.planet_id else None} 
    # for fav in favoritos]
    print(favoritos)
    return jsonify([fav.serialize() for fav in favoritos]), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_personaje_favoritos(people_id):
    add_personaje = Favoritos.query.filter_by(user_id=CURRENT_USER_ID, personajes_id = people_id).first()
    if add_personaje is None: 
        personaje = Favoritos(user_id=CURRENT_USER_ID, personajes_id= people_id)
        db.session.add(personaje)
        db.session.commit()
    return jsonify({"msg": "personaje agregado a favoritos"}),200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planet_favoritos(planet_id):
    existe = Favoritos.query.filter_by(user_id=CURRENT_USER_ID, planetas_id= planet_id).first()
    if existe is None: 
        nuevoPlanetaFavorito = Favoritos(user_id=CURRENT_USER_ID, planetas_id= planet_id)
        db.session.add(nuevoPlanetaFavorito)
        db.session.commit()
    return jsonify({"msg": "planeta agregado a favoritos"}),200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_favoritos(planet_id):
    eliminar = Favoritos.query.filter_by(user_id=CURRENT_USER_ID, planetas_id= planet_id).first()
    if eliminar: 
        db.session.delete(eliminar)
        db.session.commit()
        return jsonify({"msg": "planeta eliminado de favoritos"}),200
    
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_personaje_favoritos(people_id):
    eliminar_personaje = Favoritos.query.filter_by(user_id=CURRENT_USER_ID, personajes_id= people_id).first()
    if  eliminar_personaje: 
        db.session.delete( eliminar_personaje)
        db.session.commit()
        return jsonify({"msg": "personaje eliminado de favoritos"}),200





    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)



    # AQUI EMPIEZA EL OTRO CODIGO!!!!!

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
from models import db, User, Person, Planet, Favoritos
#from models import Person
CURRENT_USER_ID=1

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
def get_all_users():
    users = User.query.all()
    result = [user.serialize() for user in users]

    return jsonify({"result" : result})

@app.route('/signup', methods=['POST'])
def signup():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    is_active = request.json.get("is_active", True)

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"msg" : "user already exist"}), 400
    
    new_user = User(email=email, password=password, is_active=is_active)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg" : "user created successfully"}), 200

@app.route('/addperson', methods=['POST'])
def add_person():
    name = request.json.get("name", None)
    faccion = request.json.get("faccion", None)
    job = request.json.get("job", None)

    if Person.query.filter_by(name=name).first() is not None:
        return jsonify({"msg" : "person already exist"}), 400
    
    new_person = Person(name=name, faccion=faccion, job=job)
    db.session.add(new_person)
    db.session.commit()

    return jsonify({"msg" : "person created successfully"}), 200

@app.route('/addplanet', methods=['POST'])
def addplanet():
    name = request.json.get("name",None)
    temp = request.json.get("temp",None)
    size = request.json.get("size",None)

    if Planet.query.filter_by(name=name).first() is not None:
        return jsonify({"msg" : "planet already exist"})
    
    new_planet = Planet(name=name, temp=temp, size=size)
    db.session.add(new_planet)
    db.session.commit()

    return jsonify({"msg" : "planet created succesfully"})



@app.route('/people', methods=['GET'])
def get_people():
    people = Person.query.all()
    result = [person.serialize() for person in people]

    return jsonify({ "result" : result})

@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_person(people_id):
    person = Person.query.get(people_id)
    return jsonify(person.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    result = [planet.serialize() for planet in planets]
    return jsonify({"result" : result})

@app.route('/planet/<int:planet_id>',  methods=['GET'])
def get_one_planet(planet_id):
    planet = Planet.query.get(planet_id)
    return jsonify(planet.serialize())

@app.route('/user/favorites',  methods=['GET'])
def get_favorites():
    favoritos = Favoritos.query.filter_by(user_id=CURRENT_USER_ID).all()
    result = [favorito.serialize() for favorito in favoritos]
    return jsonify({"result" : result})



    

    
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

