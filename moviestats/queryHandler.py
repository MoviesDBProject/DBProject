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

    if request_array['top_actors'] == True :
        query = "SELECT youtube_id, title, rating, name
                FROM top_actors ORDER BY rating DESC LIMIT 10"

        cursor.execute(query)

        rows = dictFetchall(cursor)

        return HttpResponse(json.dumps(rows), content_type="application/json")

    example_json = {"actor": "dan",
                    "actor_birth_date": 1963,
                    "actor_birth_place": "USA",
                    "director": "tomer",
                    "film_location": "algeria",
                    "film_language": "arabic",
                    "min_views": "200000",
                    "sort": True
                    }
    cursor.execute(""" SELECT movie_url FROM trailers
 				       WHERE trailers.views_count > {0} JOIN
						(SELECT actors.movie_id as sub_movie_id FROM actors
						 WHERE actors.first_name = {1}
						JOIN movie_actor ON actors.actor_id = movie_actor.actor_id) as sub_query
					   ON trailers.movie_id = sub_query.sub_movie_id;
	                """.format(example_json["min_views"], example_json["actor"]))
    row = cursor.fetchall()


    return HttpResponse(json.dumps(rows), content_type="application/json")
