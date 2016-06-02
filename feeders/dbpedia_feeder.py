from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, RDF
from constatns import *
from youtube_handler import *

counter = 0


def get_movies_from_dbpedia():
    films_set = set()
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
                FILTER (langMatches(lang(?film_abstract),"en"))
            }LIMIT %s OFFSET %s
            """ % (end, start))
        print "[+]==== Getting movies from {0} to {1} ====[+]".format(start, end)
        sparql.setReturnFormat(JSON)
        # try:
        results = sparql.query().convert()
        fetched = 0
        # iterate over films
        for film in results["results"]["bindings"]:
            try:
                film_id = film['film_title']['value']
                if film_id not in films_set:
                    fetched += 1
                    try:
                        result = fetch_movie_info(film_id)
                        print result
                        print fetched
                    except:
                        pass
                        # print "Success score: {0}/{1}".format(counter,fetched)
                films_set.add(film_id)
            except Exception as e:
                print "Failed, Breaking"
                print str(e)
                break
    print "[+]==== Fetched {0} movies from DbPedia ====[+]".format(len(films_set))


def fetch_movie_info(url):
    global counter
    success = True
    result = {}
    uri = URIRef(url)
    graph = Graph()
    graph.parse(uri)

    for s, parent, offspring in graph:
        try:
            rdf_key_str = str(parent)  # rdf property
            rdf_val_str = str(offspring)   # value

            # check if the each of the film rdf dependencies' type is one of those we want to save
            if rdf_key_str in movieMapFromRdf.keys() and rdf_val_str != '*':
                key_in_result = movieMapFromRdf[rdf_key_str]
                if key_in_result == ACTORS:
                    if key_in_result in result:
                        result[key_in_result].append(rdf_val_str)
                    else:
                        key_in_result = movieMapFromRdf[rdf_key_str]  # is this line really needed?
                        result[key_in_result] = [rdf_val_str]
                else:
                    result[key_in_result] = rdf_val_str
        except:
            pass

    if ACTORS in result:
        result[ACTORS] = fetch_person_info(result[ACTORS])
    else:
        result[ACTORS] = {}

    if DIRECTOR in result:
        result[DIRECTOR] = fetch_person_info([result[DIRECTOR]])[0]
    else:
        result[DIRECTOR] = {}

    if LANGUAGE in result and result[LANGUAGE].startswith(DBPEDIA_PREFIX):
        result[LANGUAGE] = fetch_name_from_dbpedia_page(result[LANGUAGE])

    if COUNTRY in result and result[COUNTRY].startswith(DBPEDIA_PREFIX):
        result[COUNTRY] = fetch_name_from_dbpedia_page(result[COUNTRY])

    if success:
        counter += 1
        try:
            result[YOUTUBE] = youtube_search(result[TITLE])
        except:
            pass

        print "=============================================="
        return result


def fetch_person_info(actors_urls):
    result = []
    for actor_url in actors_urls:
        if not actor_url.startswith(DBPEDIA_PREFIX):
            result.append({NAME: actor_url})
            continue
        try:
            actor_info = {}
            uri = URIRef(actor_url)
            graph = Graph()
            graph.parse(uri)
            for s, p, o in graph:
                try:
                    rdf_key_str = str(p)
                    rdf_val_str = str(o)
                    # print "{0} : {1}".format(rdf_key_str,rdf_val_str)
                    if rdf_key_str in personMapFromRdf:
                        actor_info[personMapFromRdf[rdf_key_str]] = rdf_val_str
                except:
                    pass
            if BIRTH_PLACE in actor_info and actor_info[BIRTH_PLACE].startswith(DBPEDIA_PREFIX):
                actor_info[BIRTH_PLACE] = fetch_name_from_dbpedia_page(actor_info[BIRTH_PLACE])
            result.append(actor_info)
        except:
            pass

    return result


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
