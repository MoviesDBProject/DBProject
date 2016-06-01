from django.http import HttpResponse
from django.db import connection


def handle_query(request):
	example_json = {"actor": "dan",
	                "actor_birth_date": 1963,
	                "actor_birth_place": "USA",
	                "director": "tomer",
	                "film_location": "algeria",
	                "film_language": "arabic",
	                "min_views": "200000",
	                "sort": True
	                }

	cursor = connection.cursor()

	return HttpResponse("test")
