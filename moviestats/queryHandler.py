from django.http import HttpResponse
from django.db import connection
import json
from django.views.decorators.csrf import csrf_exempt



def dictFetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


@csrf_exempt
def init_handler(request):
    cursor = connection.cursor()
    
    body = json.loads(request.body)
    
    if body['entry'] == 'actors' or body['entry'] == 'directors' :
        query = ''' SELECT DISTINCT name as %s
                       FROM %s
                   ''' % (body['entry'].strip('s'),body['entry'])
        
        cursor.execute(query)
        rows = dictFetchall(cursor)
        
    elif body['entry'] == 'genres' :
        query = ''' SELECT DISTINCT genre
                    FROM %s
                   ''' % body['entry']
        cursor.execute(query)
        rows = dictFetchall(cursor)
                   
    else :
        query = ''' SELECT DISTINCT %s
                    FROM %s
                 ''' % (body['entry'],body['entry'])
        cursor.execute(query)
        if body['entry'] == 'language' :
            lang_set = set()
            row = cursor.fetchone()
            while row is not None:
                r = str(row).replace(' ','').strip(')').strip('(').strip('u')
                r = r.replace('\x22', '').replace('\x27','').split(',')
                
                lang_set.update(r)
                row = cursor.fetchone()
            rows = [] 
            for row in list(lang_set) :
                tmp_dict = dict()
                tmp_dict['language']= row
                rows.append(tmp_dict)
           
        else :
            rows = dictFetchall(cursor)
            
     

        
  
    return HttpResponse(json.dumps(rows), content_type="application/json")




@csrf_exempt
def handle_query(request):

    cursor = connection.cursor()

    request_array = json.loads(request.body)

    query = ""

    # Top actors
    if request_array['top_actors'] == True :
        query = """SELECT youtube_id, title, rating, name
                FROM top_actors
                ORDER BY rating DESC
                LIMIT 10"""

        cursor.execute(query)

        rows = dictFetchall(cursor)

        return HttpResponse(json.dumps(rows), content_type="application/json")

    # Creating query with search paramter
    query = "SELECT selected_movie.title, selected_movie.rating, selected_movie.actor, selected_movie.director,
            selected_movie.genre, selected_movie.country, selected_movie.language, trailers.youtube_id, trailers.view_count, "

    if request_array['max_likes'] == True :
        query += "MAX(trailers.likes) "
    else :
        query += "trailers.likes "

    query += "FROM trailers JOIN (SELECT movies.title, movies.rating, selected_actor.actor, selected_director.director,
                selected_genre.genre, selected_country.country, selected_language.language, movies.movie_id FROM movies
                JOIN (SELECT actors.name AS actor, movie_actor.movie_id
                FROM actors JOIN movie_actor ON actors.actor_id = movie_actor.actor_id "

    if request_array['actor'] != None :
        add_to_query = "WHERE actors.name = '{}'".format(request_array['actor'])
        query += add_to_query

    query += ") AS selected_actor ON movies.movie_id = selected_actor.movie_id
                JOIN (SELECT directors.name AS director, movie_director.movie_id
                FROM directors JOIN movie_director ON directors.director_id = movie_director.director_id "

    if request_array['director'] != None :
        add_to_query = "WHERE directors.name = '{}'".format(request_array['director'])
        query += add_to_query

    query += ") AS selected_director ON movies.movie_id = selected_director.movie_id
                JOIN (SELECT genres.genre, movie_genre.movie_id
              	FROM genres JOIN movie_genre ON genres.genre_id = movie_genre.genre_id "

    if request_array['film_genre'] != None :
        add_to_query = "WHERE genres.genre = '{}'".format(request_array['film_genre'])
        query += add_to_query

    query += ") AS selected_genre ON movies.movie_id = selected_genre.movie_id
                JOIN (SELECT country.country_id, country.country
              	FROM country "

    if request_array['film_location'] != None :
        add_to_query = "WHERE country.country = '{}'".format(request_array['film_location'])
        query += add_to_query

    query += ") AS selected_country ON selected_country.country_id = movies.country_id
                JOIN (SELECT language.language_id, language.language
                FROM language "

    if request_array['film_language'] != None :
        add_to_query = "WHERE language.language = '{}'".format(request_array['film_language'])
        query += add_to_query

    query += ") AS selected_language ON selected_language.language_id = movies.language_id "

    if request_array['rating'] != None :
        add_to_query = "WHERE movies.rating > {}".format(request_array['rating'])
        query += add_to_query

    query += ") AS selected_movie ON trailers.movie_id = selected_movie.movie_id "

    if request_array['min_views'] != None :
        add_to_query = "WHERE trailers.view_count > {} ".format(request_array['min_views'])
        query += add_to_query

    if request_array['max_likes'] == True :
        query += ";"
    else :
        query += "GROUP BY selected_movie.movie_id;"


    cursor.execute(query)

    rows = dictFetchall(cursor)

    return HttpResponse(json.dumps(rows), content_type="application/json")