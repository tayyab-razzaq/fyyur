from flask import render_template, request, flash, redirect, url_for
from models import *
from forms import *


# ==================================================================================================================== #
# Venues
# ==================================================================================================================== #

@app.route('/venues')
def venues():
    """
    Get list of all venues group by city.

    :return:
    """
    cities = City.query.filter(City.venues.any())
    cities_data = []
    for city in cities:
        venues_list = [venue.serialized_data for venue in city.venues]
        serialized_data = city.serialized_data
        serialized_data['venues'] = venues_list
        cities_data.append(serialized_data)

    return render_template('pages/venues.html', areas=cities_data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    """
    Get list of venue result filtered by search value.

    :return:
    """
    search_value = request.form.get('search_term', '')
    venues_list = [venue.serialized_data for venue in Venue.query.filter(Venue.name.ilike(f'%{search_value}%'))]
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
    venue = Venue.query.filter_by(id=venue_id).first()
    return render_template('pages/show_venue.html', venue=venue.serialized_data)


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    """
    Create venue from.

    :return:
    """
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    """
    Create venue using form data.

    :return:
    """
    form = VenueForm()
    if form.validate_on_submit():
        city_id = City.get_city_id(form.city.data, form.state.data)
        venue = Venue(
            name=form.name.data,
            city_id=city_id,
            address=form.address.data,
            phone=form.phone.data,
            image_link=form.image_link.data,
            facebook_link=form.facebook_link.data,
            website=form.website.data,
            seeking_description=form.seeking_description.data,
            seeking_talent=form.seeking_talent.data,
            genres=form.genres.data
        )
        # seeking talent and genre
        try:
            db.session.add(venue)
            db.session.commit()
            flash(f'Venue {venue.name} was successfully listed!')
        except:
            db.session.rollback()
            flash(f'An error occurred. Venue {venue.name} could not be listed.')
        finally:
            db.session.close()

        return render_template('pages/home.html')

    errors = form.errors

    flash('Below Errors Occurred while creating Venue')
    for key in errors.keys():
        error = errors[key]
        flash(f'{key}: f{error}')

    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    """
    Delete venue by given venue id.

    :param venue_id:
    :return:
    """
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return render_template('pages/home.html')


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    """
    Edit venue form.

    :param venue_id:
    :return:
    """
    venue = Venue.query.filter_by(id=venue_id).first()
    serialized_venue = venue.serialized_data
    form = VenueForm(obj=venue)
    form.state.process_data(serialized_venue.get('state'))
    form.city.process_data(serialized_venue.get('city'))
    return render_template('forms/edit_venue.html', form=form, venue=serialized_venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    """
    Edit venue using form data.

    :param venue_id:
    :return:
    """
    venue = Venue.query.filter_by(id=venue_id).first()
    form = VenueForm()
    if form.validate_on_submit():
        city_id = City.get_city_id(form.city.data, form.state.data)
        venue.name = form.name.data
        venue.city_id = city_id
        venue.address = form.address.data
        venue.phone = form.phone.data
        venue.image_link = form.image_link.data
        venue.facebook_link = form.facebook_link.data
        venue.website = form.website.data
        venue.seeking_description = form.seeking_description.data
        venue.seeking_talent = form.seeking_talent.data
        venue.genres = form.genres.data

        try:
            db.session.commit()
            flash(f'Venue {venue.name} was successfully listed!')
        except:
            db.session.rollback()
            flash(f'An error occurred. Venue {venue.name} could not be listed.')
        finally:
            db.session.close()

        return redirect(url_for('show_venue', venue_id=venue_id))

    errors = form.errors

    flash('Below Errors Occurred while creating Venue')
    for key in errors.keys():
        error = errors[key]
        flash(f'{key}: f{error}')

    return edit_venue(venue_id)


# ==================================================================================================================== #
# Artists
# ==================================================================================================================== #

@app.route('/artists')
def artists():
    """
    Return the list of all artists.

    :return:
    """
    artists_list = [{"id": artist.id, "name": artist.name} for artist in Artist.query.all()]
    return render_template('pages/artists.html', artists=artists_list)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    """
    Return the list of artists filtered by name based on search term.

    :return:
    """
    search_value = request.form.get('search_term', '')
    artists_list = [
        {"id": artist.id, "name": artist.name, "num_upcoming_shows": 0}
        for artist in Artist.query.filter(Artist.name.ilike(f'%{search_value}%'))]
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
    artist = Artist.query.filter_by(id=artist_id).first()
    return render_template('pages/show_artist.html', artist=artist.serialized_data)


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    """
    Edit artist form.

    :param artist_id:
    :return:
    """
    artist = Artist.query.filter_by(id=artist_id).first()
    serialized_artist = artist.serialized_data
    form = ArtistForm(obj=artist)
    form.state.process_data(serialized_artist.get('state'))
    form.city.process_data(serialized_artist.get('city'))
    return render_template('forms/edit_artist.html', form=form, artist=serialized_artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    """
    Edit artist using from data.

    :param artist_id:
    :return:
    """
    artist = Artist.query.filter_by(id=artist_id).first()
    form = VenueForm()
    if form.validate_on_submit():
        city_id = City.get_city_id(form.city.data, form.state.data)
        artist.name = form.name.data
        artist.city_id = city_id
        artist.phone = form.phone.data
        artist.image_link = form.image_link.data
        artist.facebook_link = form.facebook_link.data
        artist.website = form.website.data
        artist.seeking_description = form.seeking_description.data
        artist.seeking_venue = form.seeking_venue.data
        artist.genres = form.genres.data

        try:
            db.session.commit()
            flash(f'Artist {artist.name} was successfully listed!')
        except:
            db.session.rollback()
            flash(f'An error occurred. Artist {artist.name} could not be listed.')
        finally:
            db.session.close()

        return redirect(url_for('show_artist', artist_id=artist_id))

    errors = form.errors

    flash('Below Errors Occurred while creating Venue')
    for key in errors.keys():
        error = errors[key]
        flash(f'{key}: f{error}')

    return edit_artist(artist_id)


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    """
    Create artist form.

    :return:
    """
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    """
    Save Artist to the data base using form data.

    :return:
    """
    form = ArtistForm()
    if form.validate_on_submit():
        city_id = City.get_city_id(form.city.data, form.state.data)
        artist = Artist(
            name=form.name.data,
            city_id=city_id,
            phone=form.phone.data,
            image_link=form.image_link.data,
            facebook_link=form.facebook_link.data,
            website=form.website.data,
            seeking_description=form.seeking_description.data,
            seeking_venue=form.seeking_venue.data,
            genres=form.genres.data
        )
        try:
            db.session.add(artist)
            db.session.commit()
            flash(f'Artist {artist.name} was successfully listed!')
        except:
            db.session.rollback()
            flash(f'An error occurred. Artist {artist.name} could not be listed.')
        finally:
            db.session.close()

        return render_template('pages/home.html')

    errors = form.errors

    flash('Below Errors Occurred while creating Artist')
    for key in errors.keys():
        error = errors[key]
        flash(f'{key}: f{error}')

    return render_template('forms/new_artist.html', form=form)


# ==================================================================================================================== #
# Shows
# ==================================================================================================================== #

@app.route('/shows')
def shows():
    """
    List all shows.

    :return:
    """
    shows_data = [show.serialized_data for show in Show.query.all()]
    return render_template('pages/shows.html', shows=shows_data)


@app.route('/shows/create')
def create_shows():
    """
    Create Shows form.

    :return:
    """
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    """
    Create new show.

    :return:
    """
    form = ShowForm()
    if form.validate_on_submit():
        show = Show(
            artist_id=form.artist_id.data,
            venue_id=form.venue_id.data,
            start_time=form.start_time.data
        )
        try:
            db.session.add(show)
            db.session.commit()
            flash('Show was successfully listed!')
        except:
            db.session.rollback()
            flash(f'An error occurred. Show could not be listed.')
        finally:
            db.session.close()

        return render_template('pages/home.html')

    flash('Below Errors Occurred while creating Show')

    errors = form.errors

    for key in errors.keys():
        error = errors[key]
        flash(f'{key}: f{error}')

    return render_template('forms/new_show.html', form=form)
