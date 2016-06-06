from django.shortcuts import render

# Create your views here.


def index(request):
    context = {}
    return render(request, 'moviestats/index.html', context)


def page_not_found(request):
    context = {}
    return render(request, 'moviestats/404.html', context)


