from rdflib import Graph, URIRef, RDF

# scheme
# movie_info = {
# 					ACTORS : actors(LIST),
# 					DIRECTORS : directors(LIST),
# 					COUNTRY : country(STR),
# 					NAME : film_name(STR),
# 					ID : film_id(STR)
# 				}







DIRECTORS = "directors"
TITLE = 'title'
ACTORS = 'actors'
LANGUAGE = 'language'
CATEGORY = 'category'
ABSTRACT = 'abstract'
COUNTRY = 'country'
BIRTH_PLACE = "birth_place"
BIRTH_DATE = "birth_date"
NAME = "name"
DBPEDIA_PREFIX = "http://dbpedia"
YOUTUBE = "youtube"
WIKI_ID = 'wiki_id'
ID = 'id'
NA = 'N/A'
ITERS = 10
RANGE = 1000

movieMapFromRdf = {

	"http://dbpedia.org/ontology/director": DIRECTORS,
	"http://dbpedia.org/property/starring": ACTORS,
	"http://xmlns.com/foaf/0.1/name": TITLE,
	"http://dbpedia.org/property/language": LANGUAGE,
	"http://dbpedia.org/property/country": COUNTRY
}

personMapFromRdf = {
	"http://dbpedia.org/property/placeOfBirth": BIRTH_PLACE,
	"http://dbpedia.org/ontology/birthDate": BIRTH_DATE,
	"http://xmlns.com/foaf/0.1/name": NAME
}


# OMDB constans

OMDB_COUNTRY = 'Country'
OMDB_LANGUAGE = 'Language'
OMDB_GENRE = 'Genre'
OMDB_IMDB_RATING = 'imdbRating'
OMDB_YEAR = 'Year'
OMDB_RUNTIME = 'Runtime'
