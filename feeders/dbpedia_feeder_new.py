from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, RDF
from constatns import *
from youtube_handler import *
import urllib3
import json
import pprint
import hashlib
import sys

counter = 0
from inserts import *
import logging

# Movie id => movie url dbpedia
# Actor id => if has page ==> page link dbpedia, else id is his name
# The same for director
actors_to_fetch = []
directors_to_fetch = []
actors_to_insert = []
directors_to_insert = []


def get_movies_from_dbpedia():
	global actors_to_fetch
	global directors_to_fetch
	global actors_to_insert
	global directors_to_insert
	logging.basicConfig(filename='feeder.log', level=logging.DEBUG)
	logging.debug('[+]======= dbpedia feeder started ======[+]')
	films = set()
	films_info = []
	fetched = 0
	for i in range(ITERS):
		start = i * RANGE +START
		end = (i + 1) * RANGE + START
		sparql = SPARQLWrapper("http://dbpedia.org/sparql")

		sparql.setQuery("""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT DISTINCT ?film_name ?film_title
            GROUP_CONCAT(DISTINCT ?film_actors ; SEPARATOR = "|")
            GROUP_CONCAT(DISTINCT ?film_director ; SEPARATOR = "|")
            ?film_country
            WHERE {
                ?film_title rdf:type <http://dbpedia.org/ontology/Film> .
                ?film_title rdfs:label ?film_name .
                optional{
                   ?film_title dbp:starring ?film_actors .
                }
                optional{
                   ?film_title dbp:director ?film_director .
                }
                optional{
                   ?film_title dbp:country ?film_country .
                }
                FILTER (langMatches(lang(?film_name),"en"))
            }LIMIT %s OFFSET %s
            """ % (RANGE, start))
		print("[+]==== Getting movies from %d to %d ====[+]" % (start, end))
		logging.debug("[+]==== Getting movies from %d to %d ====[+]" % (start, end))
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()

		print len(results["results"]["bindings"])
		# iterate over films
		for film in results["results"]["bindings"]:

			try:
				film_id = str(film.get('film_title', {}).get('value', ''))
				if film_id not in films:

					try:
						movie_info = fetch_movie_info(film)
						films_info.append(movie_info)
						films.add(film_id)
						fetched += 1
						print fetched
					except Exception as e:
						print str(e)
						pass

			except Exception as e:
				# print "Failed, Breaking"
				print str(e)
				continue
		actor_in_db_count = actors_insert(actors_to_insert)
		directors_in_db_count = directors_insert(directors_to_insert)
		movies_in_db_count = movies_insert(films_info)
		logging.debug("\n\n[+]========= Movies : {0}\n[+]========= Directors : {1}\n[+]========= Actors : {2} "
		              .format(movies_in_db_count,
		                      directors_in_db_count,
		                      actor_in_db_count))
	print("[+]==== Fetched %d movies from DBPedia ====[+]" % len(films))
	return films_info


def fetch_movie_info(film):
	global counter
	global actors_to_insert
	global directors_to_insert
	success = True
	movie_info = {}

	try:
		film_id = str(film.get('film_title', {}).get('value', ''))
		actors = film.get('callret-2', {}).get('value', '').split("|")
		if "*" in actors:
			actors.remove("*")

		directors = film.get('callret-3', {}).get('value', '').split("|")
		if "*" in actors:
			directors.remove("*")

		country = film.get('film_country', {}).get('value', NA)
		film_name = film.get('film_name', {}).get('value', NA)
		movie_info = {
			ACTORS: actors,
			DIRECTORS: directors,
			COUNTRY: country,
			TITLE: film_name,
			ID: hash_func(film_id)
		}
	except Exception as e:
		print str(e)

	for person in movie_info[ACTORS]:
		if len(movie_info[ACTORS]) == 1 and movie_info[ACTORS][0] == '':
			break
		actors_to_insert.append(fetch_person_info(person))

	for person in movie_info[DIRECTORS]:
		if len(movie_info[DIRECTORS]) == 1 and movie_info[DIRECTORS][0] == '':
			break
		directors_to_insert.append(fetch_person_info(person))

	movie_info[ACTORS] = [hash_func(actor) for actor in movie_info[ACTORS]]
	movie_info[DIRECTORS] = [hash_func(director) for director in movie_info[DIRECTORS]]

	try:
		omdb_result = get_omdb(film_name)
		movie_info[COUNTRY] = omdb_result.get(OMDB_COUNTRY, NA)
		movie_info[OMDB_IMDB_RATING.lower()] = omdb_result.get(OMDB_IMDB_RATING, NA)
		movie_info[OMDB_LANGUAGE.lower()] = omdb_result.get(OMDB_LANGUAGE, NA)
		movie_info[OMDB_RUNTIME.lower()] = omdb_result.get(OMDB_RUNTIME, NA)
		temp_run_time = movie_info[OMDB_RUNTIME.lower()]

		if temp_run_time != NA and 'min' in temp_run_time:
			temp_run_time = temp_run_time.replace('min', '')
			temp_run_time = temp_run_time.strip()
			movie_info[OMDB_RUNTIME.lower()] = temp_run_time
		imdb_genre = omdb_result.get(OMDB_GENRE, NA)

		if imdb_genre != NA:
			new_imdb_genre = []
			imdb_genre = imdb_genre.split(',')
			for genre in imdb_genre:
				new_imdb_genre.append(genre.strip())
			imdb_genre = new_imdb_genre


		else:
			imdb_genre = [NA]
		movie_info[OMDB_GENRE.lower()] = imdb_genre
		movie_info[OMDB_YEAR.lower()] = omdb_result.get(OMDB_YEAR, NA)
	except Exception as e:
		print str(e)
		pass

	if success:
		counter += 1
	try:
		movie_info[YOUTUBE] = youtube_search(movie_info[TITLE] + " trailer")
	except:
		pass
	return movie_info


def hash_func(string):
	return abs(hash(string)) % (10 ** 8)


def get_omdb(film_title):
	link_omdb = "http://www.omdbapi.com/?t={0}&plot=short&r=json".format(film_title.replace(" ", "+"))
	index_of = film_title.find("(")
	if index_of:
		# if the film title contains parenthesis and a year, query OMDB with that year to avoid movies with the same name
		year_part = film_title[film_title.find("(") + 1:]
		integers_in_year_part = [int(s) for s in year_part.split(" ") if s.isdigit()]
		film_title = film_title[:film_title.find("(") - 1]
		if len(integers_in_year_part) > 0:
			year = integers_in_year_part[0]
			link_omdb = "http://www.omdbapi.com/?t={0}&y={1}&plot=short&r=json".format(film_title.replace(" ", "+"),
			                                                                           year)


	try:
		http = urllib3.PoolManager()
		r = http.request('GET', link_omdb)
	except:
		return {}
	if r.status != 200:
		return {}
	result = json.loads(r.data)
	return result


def fetch_person_info(person_dbpedia):
	result = []
	count = 0
	person_info = {}
	if person_dbpedia.startswith(DBPEDIA_PREFIX):
		id = person_dbpedia
		name = person_dbpedia[person_dbpedia.rfind("/") + 1:].replace("_", " ")
		index_of = name.find("(")
		if index_of != -1:
			name = name[:index_of]
			name = name.strip()
	else:
		name = person_dbpedia
		id = name

	person_info = {
		NAME: name,
		ID: hash_func(id)
	}

	return person_info


def fetch_name_from_dbpedia_page(url):
	uri = URIRef(url)
	graph = Graph()
	graph.parse(uri)
	for s, p, o in graph:
		try:
			rdf_key_str = str(p)
			rdf_val_str = str(o)
			if rdf_key_str in personMapFromRdf and personMapFromRdf[rdf_key_str] == NAME:
				return rdf_val_str
		except:
			pass


if __name__ == '__main__':
	get_movies_from_dbpedia()