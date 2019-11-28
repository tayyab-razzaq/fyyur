# ==================================================================================================================== #
# Imports
# ==================================================================================================================== #

from flask import Flask
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from constants import StatesEnum

# ==================================================================================================================== #
# App Config.
# ==================================================================================================================== #

app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# ==================================================================================================================== #
# Models.
# ==================================================================================================================== #

class BaseModel(db.Model):
    """Mixin / Abstract for model to add easy create and delete functionality."""
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=db.func.now())
    modified_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())


class City(BaseModel):
    """City Table."""
    __tablename__ = 'City'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    state = db.Column(db.Enum(StatesEnum))
    venues = db.relationship('Venue', backref='city')
    artists = db.relationship('Artist', backref='city')

    @classmethod
    def get_city_id(cls, city, state):
        """
        Get city id by city name and state name.

        :param city:
        :param state:
        :return:
        """
        city_instance = cls.query.filter_by(name=city, state=state).first()
        if city_instance:
            return city_instance.id

        city_instance = cls(name=city, state=state)
        try:
            db.session.add(city_instance)
            db.session.commit()
        except:
            city_instance = None
            db.session.rollback()
        finally:
            city_id = city_instance.id if city_instance else None
            db.session.close()

        return city_id

    @property
    def state_name(self):
        """
        Name of the city state.

        :return:
        """
        return self.state.name if self.state else None

    @property
    def serialized_data(self):
        """
        Serialized data of the city model instance.

        :return:
        """
        return {
            'id': self.id,
            'city': self.name,
            'state': self.state_name
        }

    def __repr__(self):
        """
        String representation of the City model instance.

        :return:
        """
        return f'<Venue {self.id} {self.name} {self.state_name}>'


class Venue(BaseModel):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city_id = db.Column(db.Integer, db.ForeignKey('City.id'))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    @property
    def serialized_data(self):
        """
        Serialized data of the venue model instance.

        :return:
        """
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'city': self.city.name,
            'state': self.city.state_name,
        }

    def __repr__(self):
        """
        String representation of the Venue model instance.

        :return:
        """
        return f'<Venue {self.id} {self.name}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(BaseModel):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    city_id = db.Column(db.Integer, db.ForeignKey('City.id'))

    @property
    def serialized_data(self):
        """
        Serialized data of the artist model instance.

        :return:
        """
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'city': self.city.name,
            'state': self.city.state_name,
        }

    def __repr__(self):
        """
        String representation of the Artist model instance.

        :return:
        """
        return f'<Artist {self.id} {self.name}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
