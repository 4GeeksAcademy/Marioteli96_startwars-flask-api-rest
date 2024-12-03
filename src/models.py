from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite = db.relationship("Favoritos",backref="user",lazy=True)


    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites": [favorite.id for favorite in self.favorite]
            # do not serialize the password, its a security breach
        }

class Personaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250),nullable=False)
    person_class = db.Column(db.String(250))
    faccion = db.Column(db.String(250))
    #RELACIONES
    favoritos = db.relationship("Favoritos",backref="personaje",lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "person_class": self.person_class,
            "faccion": self.faccion,
        }


class Planeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False,unique=True)
    temp = db.Column(db.String(50))
    descripcion = db.Column(db.String(250))
    #RELACIONES
    favoritos = db.relationship("Favoritos",backref="planeta",lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "temp": self.temp,
            "descripcion": self.descripcion
        }

class Vehiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(50),unique=True)
    size = db.Column(db.Integer)
    #RELACIONES
    favoritos = db.relationship("Favoritos",backref="vehiculo",lazy=True)

    def serialize(self):
         return {
             "id": self.id,
             "modelo": self.modelo,
             "size": self.size,
             
        }



class Favoritos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    personajes_id = db.Column(db.Integer, db.ForeignKey("personaje.id"))
    vehiculos_id = db.Column(db.Integer, db.ForeignKey("vehiculo.id"))
    planetas_id = db.Column(db.Integer, db.ForeignKey("planeta.id"))

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "personaje": self.personaje.serialize() if self.personaje else None,
            "vehiculo": self.vehiculo.serialize() if self.vehiculo else None,
            "planeta": self.planeta.serialize() if self.planeta else None
        }



