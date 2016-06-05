from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, RDF
from constatns import *
from youtube_handler import *
import urllib3
import json
import pprint
import sys
counter = 0

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
	films = set()
	films_info = []
	fetched = 0
	for i in range(ITERS):
		start = i * RANGE
		end = (i + 1) * RANGE
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
            """ % (end, start))
		print("[+]==== Getting movies from %d to %d ====[+]" % (start, end))
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()

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
						pprint.pprint(movie_info)
						print fetched
					except Exception as e:
						print str(e)
						pass
					# print "Success score: {0}/{1}".format(counter,fetched)

			except Exception as e:
				# print "Failed, Breaking"
				print str(e)
				continue
			# print("[+]==== Getting actors info ====[+]")
			# actors_to_insert = fetch_person_info(actors_to_fetch)
			# print("[+]==== Getting directors info ====[+]")
			# directors_to_insert = fetch_person_info(directors_to_fetch)

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
			ID: hash(film_id) % ((sys.maxsize + 1) * 2)
		}
	except Exception as e:
		print str(e)

	for person in movie_info[ACTORS]:
		actors_to_insert.append(fetch_person_info(person))

	for person in movie_info[DIRECTORS]:
		directors_to_insert.append(fetch_person_info(person))

	try:
		omdb_result = get_omdb(film_name)
		movie_info[COUNTRY] = omdb_result.get(OMDB_COUNTRY,NA)
		movie_info[OMDB_IMDB_RATING.lower()] = omdb_result.get(OMDB_IMDB_RATING,NA)
		movie_info[OMDB_LANGUAGE.lower()] = omdb_result.get(OMDB_LANGUAGE,NA)
		movie_info[OMDB_RUNTIME.lower()] = omdb_result.get(OMDB_RUNTIME,NA)
		imdb_genre = omdb_result.get(OMDB_GENRE,NA)
		if imdb_genre !=NA:
			imdb_genre = imdb_genre.split(',')
			for i in imdb_genre:
				i.replace(" ","")
		else:
			imdb_genre = [NA]
		movie_info[OMDB_GENRE.lower()] =imdb_genre
		movie_info[OMDB_YEAR.lower()] = omdb_result.get(OMDB_YEAR,NA)
	except Exception as e:
		print str(e)
		pass

	if success:
		counter += 1
	try:
		movie_info[YOUTUBE] = youtube_search(movie_info[TITLE] + " trailer")
	except:
		pass

	print("==============================================")
	return movie_info


def get_omdb(film_title):
	link_omdb = "http://www.omdbapi.com/?t={0}&plot=short&r=json".format(film_title.replace(" ","+"))
	index_of = film_title.find("(")
	if index_of:
		# if the film title contains parenthesis and a year, query OMDB with that year to avoid movies with the same name
		year_part = film_title[film_title.find("(")+1:]
		integers_in_year_part = [int(s) for s in year_part.split(" ") if s.isdigit()]
		film_title = film_title[:film_title.find("(") - 1]
		if len(integers_in_year_part) >0:
			year = integers_in_year_part[0]
			link_omdb = "http://www.omdbapi.com/?t={0}&y={1}&plot=short&r=json".format(film_title.replace(" ","+"),year)

	http = urllib3.PoolManager()
	r = http.request('GET', link_omdb)
	if r.status !=200:
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



	else:
		name = person_dbpedia
		id = name

	person_info = {
		NAME: name,
		ID: hash(id) % ((sys.maxsize + 1) * 2)
	}

	# pprint.pprint(person_info)
	# print "====================================="

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
