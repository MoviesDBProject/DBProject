from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, RDF


def get_movies_from_dbpedia():
	a = set()
	for i in range(40):
		start = i * 10000
		end = (i + 1) * 10000
		sparql = SPARQLWrapper("http://dbpedia.org/sparql")
		sparql.setQuery("""
		    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		    SELECT DISTINCT ?film_title ?film_abstract
			WHERE {
			?film_title rdf:type <http://dbpedia.org/ontology/Film> .
			?film_title rdfs:comment ?film_abstract
			}LIMIT %s OFFSET %s
		""" % (end, start))
		print "[+]==== Getting movies from {0} to {1} ====[+]".format(start, end)
		sparql.setReturnFormat(JSON)
		try:
			results = sparql.query().convert()
			for film in results["results"]["bindings"]:
				film_id = film['film_title']['value']
				a.add(film_id)
		except Exception as e:
			print "Failed, Breaking"
			print str(e)
			break
	print "[+]==== Fetched {0} movies from DbPedia ====[+]".format(len(a))


def fetch_movie_info(url):
	result = {}
	uri = URIRef(url)
	graph = Graph()
	graph.parse(uri)

	for s, p, o in graph:
		if p in result.keys():
			result[p].append(o)
		else:
			result[p]= [o]
	print result

if __name__ == '__main__':
	# get_movies_from_dbpedia()
	fetch_movie_info("http://dbpedia.org/resource/1001_Inventions_and_the_World_of_Ibn_Al-Haytham")
