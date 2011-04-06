from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpRequest
from recipes.models import *

# Simulate slow response from server with time.sleep(2)
# import time

def render_detail_recipe(request, recipe_id, recipe_template):
    
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    phase_list = Phase.objects.filter(recipe = recipe).order_by('ordering')
    ingredient_list = PhaseIngredient.objects.filter(phase__recipe = recipe)
    
    print phase_list
    return render_to_response(recipe_template, {
                                'recipe': recipe,
                                'phase_list': phase_list,
                                'ingredient_list': ingredient_list })

def main_page(request):
    return render_to_response('recipes/contentpage.html', { })

def list_recipes(request):
    recipe_list = Recipe.objects.all().order_by('name')
    
    if HttpRequest.is_ajax(request):
        return render_to_response('recipes/contentpage/recipe_list.html', {'recipe_list': recipe_list, })
    return render_to_response('recipes/contentpage/list.html', {'recipe_list': recipe_list, })

def search(request):
    return render_to_response('recipes/contentpage/search.html', { })

def recipe_detail(request, recipe_id):    
    return render_detail_recipe(request, recipe_id, 'recipes/contentpage/detail.html')

def active(request, recipe_id):
    #recipe = get_object_or_404(Recipe, pk=recipe_id)
    #return render_to_response('recipes/fullpage.html', { 'recipe': recipe })
    return render_detail_recipe(request, recipe_id, 'recipes/fullpage.html')

def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render_to_response('recipes/contentpage/detail.html', { 'recipe': recipe })

def new_recipe(request):
    return render_to_response('recipes/fullpage.html', { })

def user_detail(request, user_id):
    user = get_object_or_404(UserProfile, pk=user_id)
    return render_to_response('recipes/contentpage/user.html', { 'user': user })

def new_user(request):
    return render_to_response('recipes/contentpage/user.html', { })

def edit_user(request, user_id):
    user = get_object_or_404(UserProfile, pk=user_id)
    return render_to_response('recipes/contentpage/user.html', { 'user': user })

def nk_login(request):
    return render_to_response('recipes/contentpage.html', { })

def nk_logout(request):
    return render_to_response('recipes/contentpage.html', { })

def register(request):
    return render_to_response('recipes/contentpage.html', { })

def nk_help(request):
    return render_to_response('recipes/contentpage/help.html', { })

