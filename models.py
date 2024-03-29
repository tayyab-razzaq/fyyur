# ==================================================================================================================== #
# Imports
# ==================================================================================================================== #

from datetime import datetime
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
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.BOOLEAN, default=False)
    seeking_description = db.Column(db.String(500))
    genres = db.Column(db.ARRAY(db.String))

    city_id = db.Column(db.Integer, db.ForeignKey('City.id'), nullable=False)

    shows = db.relationship('Show', backref='venue')

    @property
    def upcoming_shows(self):
        """
        Get upcoming shows list of current venue.

        :return:
        """
        upcoming_shows = Show.query.filter(Show.start_time > datetime.now(), Show.venue_id == self.id).all()
        return [show.serialized_data for show in upcoming_shows]

    @property
    def past_shows(self):
        """
        Get past shows list of current venue.

        :return:
        """
        upcoming_shows = Show.query.filter(Show.start_time < datetime.now(), Show.venue_id == self.id).all()
        return [show.serialized_data for show in upcoming_shows]

    @property
    def serialized_data(self):
        """
        Serialized data of the venue model instance.

        :return:
        """
        upcoming_shows = self.upcoming_shows
        past_shows = self.past_shows

        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'city': self.city.name,
            'state': self.city.state_name,
            'genres': self.genres if self.genres else [],
            'website': self.website,
            'seeking_description': self.seeking_description,
            'seeking_talent': self.seeking_talent,
            'num_upcoming_shows': len(upcoming_shows),
            'upcoming_shows_count': len(upcoming_shows),
            'upcoming_shows': upcoming_shows,
            'past_shows': past_shows,
            'past_shows_count': len(past_shows),
        }

    def __repr__(self):
        """
        String representation of the Venue model instance.

        :return:
        """
        return f'<Venue {self.id} {self.name}>'


class Artist(BaseModel):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.BOOLEAN, default=False)
    seeking_description = db.Column(db.String(500))

    city_id = db.Column(db.Integer, db.ForeignKey('City.id'), nullable=False)

    shows = db.relationship('Show', backref='artist')

    @property
    def upcoming_shows(self):
        """
        Get upcoming shows list of current artist.

        :return:
        """
        upcoming_shows = Show.query.filter(Show.start_time > datetime.now(), Show.artist_id == self.id).all()
        return [show.serialized_data for show in upcoming_shows]

    @property
    def past_shows(self):
        """
        Get past shows list of current artist.

        :return:
        """
        upcoming_shows = Show.query.filter(Show.start_time < datetime.now(), Show.artist_id == self.id).all()
        return [show.serialized_data for show in upcoming_shows]

    @property
    def serialized_data(self):
        """
        Serialized data of the artist model instance.

        :return:
        """
        upcoming_shows = self.upcoming_shows
        past_shows = self.past_shows

        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'city': self.city.name,
            'state': self.city.state_name,
            'num_upcoming_shows': len(upcoming_shows),
            'upcoming_shows_count': len(upcoming_shows),
            'upcoming_shows': upcoming_shows,
            'past_shows': past_shows,
            'past_shows_count': len(past_shows),
        }

    def __repr__(self):
        """
        String representation of the Artist model instance.

        :return:
        """
        return f'<Artist {self.id} {self.name}>'


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime())

    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)

    @property
    def serialized_data(self):
        """
        Serialized data of the artist model instance.

        :return:
        """
        return {
            'id': self.id,
            'start_time': str(self.start_time),
            'venue_id': self.venue_id,
            'venue_name': self.venue.name,
            'venue_image_link': self.venue.image_link,
            'artist_id': self.artist_id,
            'artist_name': self.artist.name,
            'artist_image_link': self.artist.image_link
        }

    def __repr__(self):
        """
        String representation of the Show model instance.

        :return:
        """
        return f'<Show {self.id} {str(self.start_time)}>'
