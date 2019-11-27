from flask import render_template, request, flash, redirect, url_for

from dummy_data import venue, artist, shows_data

from models import *
from forms import *


# ==================================================================================================================== #
# Venues
# ==================================================================================================================== #

@app.route('/venues')
def venues():
    cities = City.query.filter(City.venues.any())
    cities_data = []
    for city in cities:
        venues_list = [venue_data.serialized_data for venue_data in city.venues]
        serialized_data = city.serialized_data
        serialized_data['venues'] = venues_list
        cities_data.append(serialized_data)

    return render_template('pages/venues.html', areas=cities_data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_value = request.form.get('search_term', '')
    venues_list = [
        venue_data.serialized_data for venue_data in Venue.query.filter(Venue.name.ilike(f'%{search_value}%'))]
    response = {
        "count": len(venues_list),
        "data": venues_list
    }
    return render_template('pages/search_venues.html', results=response, search_term=search_value)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    """
    shows the venue page with the given venue_id.

    :param venue_id:
    :return:
    """
    venue_instance = Venue.query.filter_by(id=venue_id).first()
    data = venue_instance.serialized_data
    return render_template('pages/show_venue.html', venue=data)


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))


# ==================================================================================================================== #
# Artists
# ==================================================================================================================== #

@app.route('/artists')
def artists():
    """
    Return the list of all artists.

    :return:
    """
    artists_list = [{"id": artist_data.id, "name": artist_data.name} for artist_data in Artist.query.all()]
    return render_template('pages/artists.html', artists=artists_list)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    """
    Return the list of artists filtered by name based on search term.

    :return:
    """
    search_value = request.form.get('search_term', '')
    artists_list = [{"id": artist_data.id, "name": artist_data.name, "num_upcoming_shows": 0}
                    for artist_data in Artist.query.filter(Artist.name.ilike(f'%{search_value}%'))]
    response = {
        "count": len(artists_list),
        "data": artists_list
    }
    return render_template('pages/search_artists.html', results=response, search_term=search_value)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    """
    Show the artist page by given artist_id.

    :param artist_id:
    :return:
    """
    artist_instance = Artist.query.filter_by(id=artist_id).first()
    data = artist_instance.serialized_data
    return render_template('pages/show_artist.html', artist=data)


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


# ==================================================================================================================== #
# Shows
# ==================================================================================================================== #

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data. num_shows should be aggregated based on number of upcoming shows per venue.
    return render_template('pages/shows.html', shows=shows_data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    # on successful db insert, flash success
    flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')
