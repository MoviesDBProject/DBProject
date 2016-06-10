from django.http import HttpResponse
from django.db import connection
import json
from django.views.decorators.csrf import csrf_exempt
import re
from feeders.dbpedia_feeder_new import *


def dictFetchall(cursor):
	"""Return all rows from a cursor as a dict"""
	columns = [col[0] for col in cursor.description]
	return [dict(zip(columns, row)) for row in cursor.fetchall()]


def rewrite_as_multiple_words(lang):
	words = re.findall('[A-Z][^A-Z]*', lang)
	lang = ""
	for i in range(len(words)):
		if i == len(words) - 1:
			lang += "%s" % words[i]
		else:
			lang += "%s " % words[i]
	return lang


@csrf_exempt
def init_handler(request):
	cursor = connection.cursor()

	body = json.loads(request.body)

	if body['entry'] == 'actors' or body['entry'] == 'directors':
		query = ''' SELECT DISTINCT name as %s
                       FROM %s
                   ''' % (body['entry'].strip('s'), body['entry'])

		cursor.execute(query)
		rows = dictFetchall(cursor)

	elif body['entry'] == 'genres':
		query = ''' SELECT DISTINCT genre
                    FROM %s
                   ''' % body['entry']
		cursor.execute(query)
		rows = dictFetchall(cursor)

	else:
		query = ''' SELECT DISTINCT %s
                    FROM %s
                 ''' % (body['entry'], body['entry'])
		cursor.execute(query)
		if body['entry'] == 'language':
			lang_set = set()
			row = cursor.fetchone()
			while row is not None:
				r = str(row).replace(' ', '').strip(')').strip('(').strip('u')
				r = r.replace('\x22', '').replace('\x27', '').split(',')

				lang_set.update(r)
				row = cursor.fetchone()
			rows = []
			for row in list(lang_set):
				tmp_dict = dict()
				row = rewrite_as_multiple_words(row)
				tmp_dict['language'] = row
				rows.append(tmp_dict)

		else:
			rows = dictFetchall(cursor)

	connection.close()

	return HttpResponse(json.dumps(rows), content_type="application/json")


@csrf_exempt
def handle_query(request):
	cursor = connection.cursor()

	request_array = json.loads(request.body)

	query = ""

	# Top actors
	if 'top_actors' in request_array and request_array['top_actors'] is not None:
		query = """SELECT actors.name AS actor, top_movies.youtube_id AS youtube_id, top_movies.view_count AS view_count, top_movies.title AS title, top_movies.rating AS rating
                   FROM movie_actor
                   JOIN actors
                   ON actors.actor_id = movie_actor.actor_id
                   JOIN (SELECT trailers.youtube_id, trailers.view_count, movies.title, movies.rating, movies.movie_id
                   	   FROM trailers, movies
                   	   WHERE trailers.movie_id = movies.movie_id AND movies.rating > 6 AND trailers.view_count > 100000
                       ORDER BY trailers.view_count DESC) AS top_movies
                   ON top_movies.movie_id = movie_actor.movie_id
                   GROUP BY actors.name
                   HAVING COUNT(actors.name) > 3
                   ORDER BY top_movies.rating DESC
                   LIMIT 10"""

		cursor.execute(query)

		rows = dictFetchall(cursor)

		# correcting decimal type to float(jsonable type)
		for row in rows:
			if row['rating'] is not None:
				row['rating'] = float(row['rating'])

		return HttpResponse(json.dumps(rows), content_type="application/json")

	# Creating query with search parameter
	query = """SELECT selected_movie.title, selected_movie.rating, selected_movie.actor, selected_movie.director,
                      selected_movie.genre,trailers.youtube_id, trailers.view_count, 
            """

	if 'max_likes' in request_array and request_array['max_likes'] is not None:
		query += "MAX(trailers.likes)"
	else:
		query += "trailers.likes"

	query += """
                FROM trailers 
    				 JOIN (
    				        SELECT movies.title, movies.rating, selected_actor.actor, selected_director.director,
                       selected_genre.genre, selected_country.country, selected_language.language, movies.movie_id 
                       FROM movies
                       JOIN (  SELECT actors.name AS actor, movie_actor.movie_id
                               FROM actors 
                               JOIN movie_actor ON actors.actor_id = movie_actor.actor_id 
           """

	# add a filtering where clause on actor name if requested
	if 'actor' in request_array and request_array['actor'] is not None:
		add_to_query = "WHERE actors.name = '{}'".format(request_array['actor'])
		query += add_to_query

	query += """
                ) AS selected_actor ON movies.movie_id = selected_actor.movie_id
                JOIN (
                      SELECT directors.name AS director, movie_director.movie_id
                      FROM directors 
                      JOIN movie_director ON directors.director_id = movie_director.director_id 
             """

	# add a filtering where clause on director's name if requested
	if 'director' in request_array and request_array['director'] is not None:
		add_to_query = "WHERE directors.name = '{}'".format(request_array['director'])
		query += add_to_query

	query += """) AS selected_director ON movies.movie_id = selected_director.movie_id
                JOIN (SELECT genres.genre, movie_genre.movie_id
              	FROM genres JOIN movie_genre ON genres.genre_id = movie_genre.genre_id """

	# add a filtering where clause on film genre if requested
	if 'film_genre' in request_array and request_array['film_genre'] is not None:
		add_to_query = "WHERE genres.genre = '{}'".format(request_array['film_genre'])
		query += add_to_query

	query += """
                ) AS selected_genre ON movies.movie_id = selected_genre.movie_id
                JOIN (SELECT country.country_id, country.country
              	       FROM country
              """

	# add a filtering where clause on country if requested
	if 'film_location' in request_array and request_array['film_location'] is not None:
		add_to_query = "WHERE country.country = '{}'".format(request_array['film_location'])
		query += add_to_query

	query += """
                ) AS selected_country ON selected_country.country_id = movies.country_id
                JOIN (SELECT language.language_id, language.language
                      FROM language """

	# add a filtering where clause on film language if requested
	if 'film_language' in request_array and request_array['film_language'] is not None:
		add_to_query = "WHERE language.language LIKE '%{}%'".format(request_array['film_language'])
		query += add_to_query

	query += """
               ) AS selected_language ON selected_language.language_id = movies.language_id
             """

	# add a filtering where clause on film IMDb Rating if requested
	if 'rating' in request_array and request_array['rating'] is not None:
		add_to_query = "WHERE movies.rating > {}".format(request_array['rating'])
		query += add_to_query

	# closing the first JOIN
	query += """
                ) AS selected_movie
              ON trailers.movie_id = selected_movie.movie_id 
             """

	# add a filtering where clause on the movie's trailer youtube views if requested
	if 'min_views' in request_array and request_array['min_views'] is not None:
		add_to_query = "WHERE trailers.view_count >= {} ".format(request_array['min_views'])
		query += add_to_query

	if 'max_likes' in request_array and request_array['max_likes'] is not None:
		query += "GROUP BY trailers.likes;"
	else:
		query += "GROUP BY selected_movie.movie_id;"

	cursor.execute(query)

	rows = dictFetchall(cursor)

	# correcting decimal type to float(jsonable type)
	for row in rows:
		if row['rating'] is not None:
			row['rating'] = float(row['rating'])

	connection.close()

	return HttpResponse(json.dumps(rows), content_type="application/json")


@csrf_exempt
def update_db(request):
	'''
	Runs the feeder that updates/feeds the db with the most recect movies in DB pedia

	'''

	request_array = json.loads(request.body)
	if 'token' in request_array and request_array['token'] == 'DbMysql03':
		get_movies_from_dbpedia()
		resopnse = {'status': 'OK'}

	else:
		resopnse = {'status': 'NOK'}

	return HttpResponse(json.dumps(resopnse), content_type="application/json")
