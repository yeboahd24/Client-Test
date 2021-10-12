from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1><b> Welcome to Djangos's Git Repository</b></h1>")