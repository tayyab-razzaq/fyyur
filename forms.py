from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField
from wtforms.validators import DataRequired, URL
from constants import STATES, GENRES


class ShowForm(Form):
    artist_id = StringField('artist_id')
    venue_id = StringField('venue_id')
    start_time = DateTimeField('start_time', validators=[DataRequired()], default=datetime.today())


class VenueForm(Form):
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField('state', validators=[DataRequired()], choices=STATES)
    address = StringField('address', validators=[DataRequired()])
    phone = StringField('phone')
    image_link = StringField('image_link')
    # TODO implement enum restriction
    genres = SelectMultipleField('genres', validators=[DataRequired()], choices=GENRES)
    facebook_link = StringField('facebook_link', validators=[URL()])


class ArtistForm(Form):
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField('state', validators=[DataRequired()], choices=STATES)
    # TODO implement validation logic for state
    phone = StringField('phone')
    image_link = StringField('image_link')
    # TODO implement enum restriction
    genres = SelectMultipleField('genres', validators=[DataRequired()], choices=GENRES)
    # TODO implement enum restriction
    facebook_link = StringField('facebook_link', validators=[URL()])

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
