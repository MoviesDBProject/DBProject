from django.http import HttpResponse
import mysql.connector

def handle_query(request):
	example_json = {"actor": "dan",
	                "actor_birth_date": 1963,
	                "actor_birth_place": "USA",
	                "director": "tomer",
	                "film_location": "algeria",
	                "film_language": "arabic",
	                "min_views": "200000",
	                "sort":True
}



	return HttpResponse("test")
