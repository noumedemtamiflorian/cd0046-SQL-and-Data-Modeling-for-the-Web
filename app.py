#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

from config import SQLALCHEMY_DATABASE_URI, DEBUG
from flask_migrate import Migrate

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO connect to a local postgresql database

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

show_artists = db.Table('show_artists',
                        db.Column('artist_id', db.Integer, db.ForeignKey(
                            'artists.id'), primary_key=True),
                        db.Column('show_id', db.Integer, db.ForeignKey(
                            'shows.id'), primary_key=True)
                        )

show_venues = db.Table('show_venues',
                       db.Column('venue_id', db.Integer, db.ForeignKey(
                           'venues.id'), primary_key=True),
                       db.Column('show_id', db.Integer, db.ForeignKey(
                           'shows.id'), primary_key=True)
                       )


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))

    shows = db.relationship(
        'Show', secondary=show_venues, backref=db.backref("venues", lazy=True))

    def __repr__(self):
        return "<Venue ID: "+str(self.id)+", name: "+str(self.name)+">"

    @property
    def upcoming_shows(self):
        results = []
        for show in self.shows:
            if show.start_time >= datetime.today():
                results.append({
                    "artist_id":  str(show.artists[0].id),
                    "artist_name": str(show.artists[0].name),
                    "artist_image_link": str(show.artists[0].image_link),
                    "start_time":  str(show.start_time)
                })
        return results

    @property
    def past_shows(self):
        results = []
        for show in self.shows:
            if show.start_time < datetime.today():
                results.append({
                    "artist_id":  str(show.artists[0].id),
                    "artist_name": str(show.artists[0].name),
                    "artist_image_link": str(show.artists[0].image_link),
                    "start_time":  str(show.start_time)
                })
        return results


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO implement any missing fields, as a database migration using Flask-Migrate

    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))

    shows = db.relationship(
        'Show', secondary=show_artists, backref=db.backref("artists", lazy=True))

    def __repr__(self):
        return "<Artist ID: "+str(self.id)+", name: "+str(self.name)+">"

    @property
    def upcoming_shows(self):
        results = []
        for show in self.shows:
            if show.start_time >= datetime.today():
                results.append({
                    "venue_id":  str(show.venues[0].id),
                    "venue_name": str(show.venues[0].name),
                    "venue_image_link": str(show.venues[0].image_link),
                    "start_time":  str(show.start_time)
                })
        return results

    @property
    def past_shows(self):
        results = []
        for show in self.shows:
            if show.start_time < datetime.today():
                results.append({
                    "venue_id":  str(show.venues[0].id),
                    "venue_name": str(show.venues[0].name),
                    "venue_image_link": str(show.venues[0].image_link),
                    "start_time":  str(show.start_time)
                })
        return results

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)

    def __repr__(self):
        return "<Show ID: "+str(self.id)+", start time: "+str(self.start_time)+">"


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    data = [{
        "city": "San Francisco",
        "state": "CA",
        "venues": [{
            "id": 1,
            "name": "The Musical Hop",
            "num_upcoming_shows": 0,
        }, {
            "id": 3,
            "name": "Park Square Live Music & Coffee",
            "num_upcoming_shows": 1,
        }]
    }, {
        "city": "New York",
        "state": "NY",
        "venues": [{
            "id": 2,
            "name": "The Dueling Pianos Bar",
            "num_upcoming_shows": 0,
        }]
    }]
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    search_term = request.form.get('search_term', '')

    venues = []

    for venue in Venue.query.all():
        if str(venue.name).upper().find(str(search_term).upper()) != -1:
            venues.append({
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": len(venue.upcoming_shows)
            })

    response = {
        "count": len(venues),
        "data": venues
    }
    return render_template('pages/search_venues.html', results=response, search_term=search_term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO replace with real venue data from the venues table, using venue_id

    venue = Venue.query.get(venue_id)
    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": venue.past_shows,
        "upcoming_shows": venue.upcoming_shows,
        "past_shows_count": len(venue.past_shows),
        "upcoming_shows_count": len(venue.upcoming_shows),
    }

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO  insert form data as a new Venue record in the db, instead
    error = False
    try:
        seeking_talent = False
        for i in request.form:
            if i == 'seeking_talent':
                seeking_talent = True

        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        address = request.form['address']
        phone = request.form['phone']
        image_link = request.form['image_link']
        facebook_link = request.form['facebook_link']
        genres = request.form['genres']
        website_link = request.form['website_link']
        seeking_description = request.form['seeking_description']

        venue = Venue(name=name, city=city, state=state, address=address, phone=phone, image_link=image_link, facebook_link=facebook_link,
                      genres=genres, website_link=website_link, seeking_talent=seeking_talent,  seeking_description=seeking_description)

    # TODO modify data to be the data object returned from db insertion

        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')

    # TODO on unsuccessful db insert, flash an error instead.
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info())
        flash('An error occurred. Venue ' +
              data.name + ' could not be listed.')
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # TODO replace with real data returned from querying the database

    artists = Artist.query.all()
    datas = []
    for artist in artists:
        datas.append({
            "id": artist.id,
            "name": artist.name
        })

    return render_template('pages/artists.html', artists=datas)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term', '')

    artists = []

    for artist in Artist.query.all():

        if str(artist.name).upper().find(str(search_term).upper()) != -1:
            artists.append({
                "id": artist.id,
                "name": artist.name,
                "num_upcoming_shows": len(artist.upcoming_shows)
            })

    response = {
        "count": len(artists),
        "data": artists
    }
    return render_template('pages/search_artists.html', results=response, search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO replace with real artist data from the artist table, using artist_id

    artist = Artist.query.get(artist_id)

    data = {
        "id": artist.id,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": artist.past_shows,
        "upcoming_shows": artist.upcoming_shows,
        "past_shows_count": len(artist.past_shows),
        "upcoming_shows_count": len(artist.upcoming_shows),
    }

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    data = Artist.query.get(artist_id)
    form = ArtistForm(obj=data)

    # TODO populate form with fields from artist with ID <artist_id>

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

    venue = Venue.query.get(venue_id)

    form = VenueForm(obj=venue)
    # TODO populate form with values from venue with ID <venue_id>

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO insert form data as a new Venue record in the db, instead
    error = False
    try:
        seeking_venue = False
        for i in request.form:
            if i == 'seeking_venue':
                seeking_venue = True

        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        phone = request.form['phone']
        image_link = request.form['image_link']
        facebook_link = request.form['facebook_link']
        genres = request.form['genres']
        website_link = request.form['website_link']
        seeking_description = request.form['seeking_description']

        artist = Artist(name=name, city=city, state=state, phone=phone, image_link=image_link, facebook_link=facebook_link,
                        genres=genres, website_link=website_link, seeking_venue=seeking_venue,  seeking_description=seeking_description)
    # TODO modify data to be the data object returned from db insertion

        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')

    # TODO on unsuccessful db insert, flash an error instead.
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info())
        flash('An error occurred. Venue ' +
              data.name + ' could not be listed.')
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------


@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO replace with real venues data.
    shows = Show.query.all()
    data = []
    for show in shows:
        data.append({
                    "venue_id": show.venues[0].id,
                    "venue_name": show.venues[0].name,
                    "artist_id": show.artists[0].id,
                    "artist_name": show.artists[0].name,
                    "artist_image_link": show.artists[0].image_link,
                    "start_time": str(show.start_time)
                    })

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():

    # TODO insert form data as a new Show record in the db, instead
    error = False
    try:
        artist_id = request.form['artist_id']
        venue_id = request.form['venue_id']
        start_time = request.form['start_time']

        show = Show(start_time=start_time)
        artist = Artist.query.get(artist_id)
        venue = Venue.query.get(venue_id)

        artist.shows.append(show)
        venue.shows.append(show)

    # TODO on unsuccessful db insert, flash an error instead.

        db.session.commit()
        flash('Show was successfully listed!')

    except():
        db.session.rollback()
        error = True
        print(sys.exc_info())
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
