from rdflib import Graph, URIRef, RDF

DIRECTOR = "director"
TITLE = 'title'
ACTORS = 'actors'
LANGAUAGE = 'language'
CATEGORY = 'category'
ABSTRACT = 'abstract'
COUNTRY = 'country'
BIRTH_PLACE = "birth_place"
BIRTH_DATE = "birth_date"
NAME = "name"
DBPEDIA_PREFIX = "http://dbpedia"


movieMapFromRdf = {
	"http://dbpedia.org/ontology/director":DIRECTOR,
	"http://dbpedia.org/property/starring":ACTORS,

	"http://xmlns.com/foaf/0.1/name":TITLE,
	"http://dbpedia.org/property/language":LANGAUAGE,
	"http://dbpedia.org/ontology/abstract":ABSTRACT,
	"http://dbpedia.org/property/country":COUNTRY
}
personMapFromRdf = {
	"http://dbpedia.org/property/placeOfBirth":BIRTH_PLACE,
	"http://dbpedia.org/ontology/birthDate":BIRTH_DATE,
	"http://xmlns.com/foaf/0.1/name":NAME
}