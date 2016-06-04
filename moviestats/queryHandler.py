from django.http import HttpResponse
from django.db import connection
# * Movies (Movie ID, title, Language ID, Country ID, Budget, Runtime,Last updated)
#
# * Actors (Actor ID, first name, last name, birthplace, DateOfBirth, last updated )
#
# * Director (Director ID, first name, last name, Movie ID)
#
# * MovieActor (Actor ID, Movie ID)
#
# * Movie_Descreption (Movie ID, title, description)
#
# * Country (Country ID, name, last updated)
#
# * Language (Language ID, language)
#
# * Trailers (YouTube ID, title, Movie_ID, Category ID, views count, likes)
#
# * Categories ( Category ID , Name)


def dictFetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_actors(request):
    cursor = connection.cursor()

    actors_query = ''' SELECT DISTINCT first_name as actor_fname,last_name as actor_last_name,
                              birthplace as actor_birth_place, DateOfBirth as actor_birth_date
                       FROM Actors
                   '''

    cursor.execute(actors_query)
    rows = dictFetchall(cursor)

    return HttpResponse(rows)


def get_directors(request):
    cursor = connection.cursor()

    director_query = ''' SELECT DISTINCT first_name , last_name
                       FROM Director
                   '''

    cursor.execute(director_query)
    rows = [{"director":(row.first_name + row.last_name} for row in dictFetchall(cursor)]
    return HttpResponse(rows)

def get_languages(request):

    cursor = connection.cursor()
    query = ''' SELECT DISTINCT language
                         FROM Language
                      '''

    cursor.execute(query)
    rows = cursor.fetchall()
    return HttpResponse(rows)


def get_countries(request):

    cursor = connection.cursor()
    query = ''' SELECT DISTINCT name
                         FROM Country
                      '''

    cursor.execute(query)
    rows = cursor.fetchall()
    return HttpResponse(rows)

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
