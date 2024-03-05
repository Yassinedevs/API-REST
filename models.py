from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Planets(db.Model):
    __tablename__ = 'planets'

    idPlanet = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    climate = db.Column(db.String(255))
    surfaceWater = db.Column(db.String(255))
    diameter = db.Column(db.Integer)
    rotationPeriod = db.Column(db.Integer)
    created = db.Column(db.DateTime, nullable=False)
    terrain = db.Column(db.String(255))
    gravity = db.Column(db.String(255))
    orbitalPeriod = db.Column(db.Integer)
    population = db.Column(db.Integer)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_one_by_id(cls, id):
        return cls.query.filter(Planets.idPlanet==id).first()


class Films(db.Model):
    idFilm = db.Column(db.Integer, primary_key=True)
    edited = db.Column(db.DateTime, nullable=False)
    producer = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    episodeId = db.Column(db.Integer, nullable=False)
    director = db.Column(db.String(255), nullable=False)
    releaseDate = db.Column(db.Date, nullable=False)
    openingCrawl = db.Column(db.Text, nullable=False)

    species = db.relationship('FilmsSpecies', backref='films_species', lazy=True)
    planets = db.relationship('FilmsPlanets', backref='films_planets', lazy=True)
    people = db.relationship('FilmsPeople', backref='films_people', lazy=True)
    starships = db.relationship('FilmsStarships', backref='films_starships', lazy=True)
    
    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_one_by_id(cls, id):
        return cls.query.filter(Films.idFilm==id).first()

class People(db.Model):
    __tablename__ = 'people'

    idPeople = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    skinColor = db.Column(db.String(255))
    hairColor = db.Column(db.String(255))
    height = db.Column(db.String(255))
    eyeColor = db.Column(db.String(255))
    mass = db.Column(db.String(255))
    birthYear = db.Column(db.String(255))
    created = db.Column(db.DateTime, nullable=False)
    edited = db.Column(db.DateTime, nullable=False)

    idPlanet = db.Column(db.Integer, db.ForeignKey('planets.idPlanet'), nullable=False)
    idStarship = db.Column(db.Integer, db.ForeignKey('starships.idStarship'))
    idVehicle = db.Column(db.Integer, db.ForeignKey('vehicles.idVehicle'))
    
    planet = db.relationship('Planets', backref='people')
    starship = db.relationship('Starships', backref='people')
    vehicle = db.relationship('Vehicles', backref='people')

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_one_by_id(cls, id):
        return cls.query.filter(People.idPeople==id).first()
    
   

class Species(db.Model):
    __tablename__ = 'species'

    idSpecie = db.Column(db.Integer, primary_key=True)
    classification = db.Column(db.String(255))
    name = db.Column(db.String(255))
    designation = db.Column(db.String(255))
    created = db.Column(db.DateTime, nullable=False)
    edited = db.Column(db.DateTime, nullable=False)
    eyeColors = db.Column(db.String(255))
    people = db.Column(db.String(255))
    skinColors = db.Column(db.String(255))
    language = db.Column(db.String(255))
    hairColors = db.Column(db.String(255))
    averageLifespan = db.Column(db.String(255))
    averageHeight = db.Column(db.String(255))

    idPlanet = db.Column(db.Integer, db.ForeignKey('planets.idPlanet'))
    planet = db.relationship('Planets', backref='species')

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_one_by_id(cls, id):
        return cls.query.filter(Species.idSpecie==id).first()

class Starships(db.Model):
    __tablename__ = 'starships'

    idStarship = db.Column(db.Integer, primary_key=True)
    MGLT = db.Column(db.String(255), nullable=False)
    starshipClass = db.Column(db.String(255), nullable=False)
    hyperdriveRating = db.Column(db.String(255), nullable=False)

    idTransport = db.Column(db.Integer, db.ForeignKey('transport.idTransport'))
    transport = db.relationship('Transport', backref='starships')
    
    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_one_by_id(cls, id):
        return cls.query.filter(Starships.idStarship==id).first()
    

class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    idVehicle = db.Column(db.Integer, primary_key=True)
    vehicleClass = db.Column(db.String(255), nullable=False)

    idTransport = db.Column(db.Integer, db.ForeignKey('transport.idTransport'))
    transport = db.relationship('Transport', backref='vehicles')
    
    @classmethod
    def get_all(cls):
        return cls.query.all()


class Transport(db.Model):
    __tablename__ = 'transport'

    idTransport = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    model = db.Column(db.String(255))
    manufacturer = db.Column(db.String(255))
    costInCredits = db.Column(db.String(255))
    length = db.Column(db.String(255))
    maxAtmospheringSpeed = db.Column(db.String(255))
    crew = db.Column(db.String(255))
    passengers = db.Column(db.String(255))
    cargoCapacity = db.Column(db.String(255))
    consumables = db.Column(db.String(255))
    created = db.Column(db.DateTime, nullable=False)
    edited = db.Column(db.DateTime, nullable=False)

    @classmethod
    def get_one_by_id(cls, id):
        return cls.query.filter(Transport.idTransport==id).first()


class FilmsPeople(db.Model):
    __tablename__ = 'filmspeople'

    idPeople = db.Column(db.Integer, db.ForeignKey('people.idPeople'), primary_key=True)
    idFilm = db.Column(db.Integer, db.ForeignKey('films.idFilm'), primary_key=True)

    film = db.relationship('Films', backref='films_people')
    people = db.relationship('People', backref='films_people')

class FilmsPlanets(db.Model):
    __tablename__ = 'filmsplanets'

    idPlanet = db.Column(db.Integer, db.ForeignKey('planets.idPlanet'), primary_key=True)
    idFilm = db.Column(db.Integer, db.ForeignKey('films.idFilm'), primary_key=True)

    film = db.relationship('Films', backref='films_planets')
    planet = db.relationship('Planets', backref='films_planets')


class FilmsSpecies(db.Model):
    __tablename__ = 'filmsspecies'

    idSpecie = db.Column(db.Integer, db.ForeignKey('species.idSpecie'), primary_key=True)
    idFilm = db.Column(db.Integer, db.ForeignKey('films.idFilm'), primary_key=True)

    film = db.relationship('Films', backref='films_species')
    specie = db.relationship('Species', backref='films_species')


class FilmsStarships(db.Model):
    __tablename__ = 'filmsstarships'

    idStarship = db.Column(db.Integer, db.ForeignKey('starships.idStarship'), primary_key=True)
    idFilm = db.Column(db.Integer, db.ForeignKey('films.idFilm'), primary_key=True)

    film = db.relationship('Films', backref='films_starships')
    starship = db.relationship('Starships', backref='films_starships')


class FilmsVehicles(db.Model):
    __tablename__ = 'filmsvehicles'

    idVehicle = db.Column(db.Integer, db.ForeignKey('vehicles.idVehicle'), primary_key=True)
    idFilm = db.Column(db.Integer, db.ForeignKey('films.idFilm'), primary_key=True)

    film = db.relationship('Films', backref='films_vehicles')
    vehicle = db.relationship('Vehicles', backref='films_vehicles')



class PeopleSpecies(db.Model):
    __tablename__ = 'peoplespecies'

    idPeople = db.Column(db.Integer, db.ForeignKey('people.idPeople'), primary_key=True)
    idSpecie = db.Column(db.Integer, db.ForeignKey('species.idSpecie'), primary_key=True)

    people = db.relationship('People', backref='people_species')
    specie = db.relationship('Species', backref='people_species')


class User(db.Model):
    idUser = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)