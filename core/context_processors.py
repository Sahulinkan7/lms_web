from django.shortcuts import render
from storeapp.models import Categories

def all_courses(request):
    categories=Categories.objects.all()
    return {'categories':categories}