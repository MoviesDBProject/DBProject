from django.shortcuts import render

# Create your views here.


def index(request):
    context = {}
    return render(request, 'moviestats/index.html', context)

#    return HttpResponse("Hello, world. You're at the polls index.")
