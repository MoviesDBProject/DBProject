from django.http import HttpResponse
from django.db import connection
import json
# * Movies (Movie ID, title, Language ID, Country ID,Category ID, Last updated)
#
# * Actors (Actor ID, first name, last name, last updated )
#
# * Director (Director ID, first name, last name, Movie ID)
#
# * MovieActor (Actor ID, Movie ID)
#
# * Movie_Description (Movie ID, title, description)
#
# * Country (Country ID, name, last updated)
#
# * Language (Language ID, language)
#
# * Trailers (YouTube ID, title, Movie_ID, views count, likes)
#
# * Categories ( Category ID , Name)


def dictFetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_actors(request):
    cursor = connection.cursor()

    actors_query = ''' SELECT DISTINCT actors.name as actor_name
                       FROM actors
                   '''

    cursor.execute(actors_query)
    rows = dictFetchall(cursor)

    return HttpResponse(json.dumps(rows))


def get_directors(request):
    cursor = connection.cursor()

    director_query = ''' SELECT DISTINCT director.name
                       FROM director
                   '''

    cursor.execute(director_query)
    rows = dictFetchall(cursor)
    return HttpResponse(json.dumps(rows))

def get_languages(request):

    cursor = connection.cursor()
    query = ''' SELECT DISTINCT language.language
                         FROM language
                '''

    cursor.execute(query)
    rows = cursor.fetchall()
    return HttpResponse(json.dumps(rows))


def get_countries(request):

    cursor = connection.cursor()
    query = ''' SELECT DISTINCT country.name
                         FROM country
                      '''

    cursor.execute(query)
    rows = cursor.fetchall()
    return HttpResponse(json.dumps(rows))


def handle_query(request):
    example_json = {"actor": "dan",
                    "actor_birth_date": 1963,
                    "actor_birth_place": "USA",
                    "director": "tomer",
                    "film_location": "algeria",
                    "film_language": "arabic",
                    "min_views": "200000",
                    "sort": True
                    }

    cursor = connection.cursor()
    cursor.execute(""" SELECT movie_url FROM trailers
 				       WHERE trailers.views_count > {0} JOIN
						(SELECT actors.movie_id as sub_movie_id FROM actors
						 WHERE actors.first_name = {1}
						JOIN movie_actor ON actors.actor_id = movie_actor.actor_id) as sub_query
					   ON trailers.movie_id = sub_query.sub_movie_id;
	                """.format(example_json["min_views"], example_json["actor"]))
    row = cursor.fetchall()
    return HttpResponse("test")
