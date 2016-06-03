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
