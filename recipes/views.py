from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpRequest
from recipes.models import Recipe

# Simulate slow response from server with time.sleep(2)
# import time

def base(request):
    return render_to_response('recipes/contentpage.html', { })

def list(request):
    recipe_list = Recipe.objects.all().order_by('name')
    
    if HttpRequest.is_ajax(request):
        return render_to_response('recipes/contentpage/recipe_list.html', {'recipe_list': recipe_list, })
    return render_to_response('recipes/contentpage/list.html', {'recipe_list': recipe_list, })

def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render_to_response('recipes/contentpage/detail.html', { 'recipe': recipe })
