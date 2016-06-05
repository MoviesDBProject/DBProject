from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, RDF
from constatns import *
from youtube_handler import *
import urllib2,json

counter = 0

# Movie id => movie url dbpedia
# Actor id => if has page ==> page link dbpedia, else id is his name
# The same for director

def get_movies_from_dbpedia():
    films = set()
    films_info = []
    for i in range(ITERS):
        start = i * RANGE
        end = (i + 1) * RANGE
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")

        sparql.setQuery("""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT DISTINCT ?film_name
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
                   ?film_title dbp:country ?film_country
                }

                FILTER (langMatches(lang(?film_name),"en"))


            }LIMIT %s OFFSET %s
            """ % (end, start))
        print("[+]==== Getting movies from %d to %d ====[+]" %(start, end))
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        fetched= 0
        # iterate over films
        for film in results["results"]["bindings"]:
            try:
                film_id = film['film_title']['value']
                if film_id not in films:
                    fetched += 1
                    try:
                        movie_info = fetch_movie_info(film_id)
                        movie_info[ABSTRACT] = film['film_abstract']['value']
                        # movie_info[WIKI_ID] = get_wiki_id(movie_info[TITLE])
                        films_info.append(movie_info)
                        films.add(film_id)
                        print movie_info
                        print fetched
                    except:
                        pass
                        # print "Success score: {0}/{1}".format(counter,fetched)

            except Exception as e:
                print "Failed, Breaking"
                print str(e)
                break

    print("[+]==== Fetched %d movies from DBPedia ====[+]" % len(films))
    return films_info


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
            if rdf_key_str in movieMapFromRdf and rdf_val_str != '*':
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
        result[ACTORS] = []

    if DIRECTOR in result:
        result[DIRECTOR] = fetch_person_info([result[DIRECTOR]])[0]
    else:
        result[DIRECTOR] = []

    if LANGUAGE in result and result[LANGUAGE].startswith(DBPEDIA_PREFIX):
        result[LANGUAGE] = fetch_name_from_dbpedia_page(result[LANGUAGE])

    if COUNTRY in result and result[COUNTRY].startswith(DBPEDIA_PREFIX):
        result[COUNTRY] = fetch_name_from_dbpedia_page(result[COUNTRY])

    if success:
        counter += 1
    try:
        result[YOUTUBE] = youtube_search(result[TITLE] + " trailer")
    except:
        pass

    print("==============================================")
    return result


def fetch_person_info(persons_urls):
    result = []
    for person_url in persons_urls:
        if not person_url.startswith(DBPEDIA_PREFIX):
            return {NAME: person_url}

        try:
            person_info = {}
            uri = URIRef(person_url)
            graph = Graph()
            graph.parse(uri)
            for s, p, o in graph:
                try:
                    rdf_key_str = str(p)
                    rdf_val_str = str(o)
                    # print "{0} : {1}".format(rdf_key_str,rdf_val_str)
                    if rdf_key_str in personMapFromRdf:
                        person_info[personMapFromRdf[rdf_key_str]] = rdf_val_str
                except:
                    pass
            if BIRTH_PLACE in person_info and person_info[BIRTH_PLACE].startswith(DBPEDIA_PREFIX):
                person_info[BIRTH_PLACE] = fetch_name_from_dbpedia_page(person_info[BIRTH_PLACE])

            # person_info[WIKI_ID] = get_wiki_id(person_info[NAME])
            result.append(person_info)
        except:
            pass

    return result


def get_wiki_id(name):
    name = name.replace(" ", "_")
    wiki_id = urllib2.urlopen('https://en.wikipedia.org/w/api.php?action=query&titles=%s&format=json' % name)
    json_id = json.load(wiki_id)
    return json_id['query']['pages'].keys()[0]





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
