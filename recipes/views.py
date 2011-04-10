from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpRequest, HttpResponseRedirect
from recipes.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.template import RequestContext

# Simulate slow response from server with time.sleep(2)
# import time

def menu(request):
    return render_to_response('recipes/contentpage/menu.html', { }, context_instance=RequestContext(request))

def render_detail_recipe(request, recipe_id, recipe_template):
    
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    phase_list = Phase.objects.filter(recipe = recipe).order_by('ordering')
    ingredient_list = PhaseIngredient.objects.filter(phase__recipe = recipe)
    
    print phase_list
    return render_to_response(recipe_template, {
                                'recipe': recipe,
                                'phase_list': phase_list,
                                'ingredient_list': ingredient_list }, context_instance=RequestContext(request))

def main_page(request):
    return render_to_response('recipes/contentpage.html', { }, context_instance=RequestContext(request))

def list_recipes(request):
    recipe_list = Recipe.objects.all().order_by('name')
    
    if HttpRequest.is_ajax(request):
        return render_to_response('recipes/contentpage/recipe_list.html', {'recipe_list': recipe_list, }, context_instance=RequestContext(request))
    return render_to_response('recipes/contentpage/list.html', {'recipe_list': recipe_list, }, context_instance=RequestContext(request))

def search(request):
    return render_to_response('recipes/contentpage/search.html', { }, context_instance=RequestContext(request))

def recipe_detail(request, recipe_id):    
    return render_detail_recipe(request, recipe_id, 'recipes/contentpage/detail.html', context_instance=RequestContext(request))

def active(request, recipe_id):
    #recipe = get_object_or_404(Recipe, pk=recipe_id)
    #return render_to_response('recipes/fullpage.html', { 'recipe': recipe })
    return render_detail_recipe(request, recipe_id, 'recipes/fullpage.html', context_instance=RequestContext(request))

def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render_to_response('recipes/contentpage/detail.html', { 'recipe': recipe }, context_instance=RequestContext(request))

def new_recipe(request):
    return render_to_response('recipes/fullpage.html', { }, context_instance=RequestContext(request))

def user_detail(request, user_id):
    user = get_object_or_404(UserProfile, pk=user_id)
    return render_to_response('recipes/contentpage/user.html', { 'user': user }, context_instance=RequestContext(request))

def new_user(request):
    return render_to_response('recipes/contentpage/user.html', { }, context_instance=RequestContext(request))

def edit_user(request, user_id):
    user = get_object_or_404(UserProfile, pk=user_id)
    return render_to_response('recipes/contentpage/user.html', { 'user': user }, context_instance=RequestContext(request))

# This is currently not in use
def nk_login(request):
    return render_to_response('recipes/contentpage.html', { })

def nk_logout(request):
    return render_to_response('recipes/contentpage.html', { })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1']) # POST has password data for both fields!
            login(request, new_user)
            return HttpResponseRedirect("/")
        else:
            # Show error page
            pass
    else:
        form = UserCreationForm()
    return render_to_response("recipes/contentpage/register.html", {
                            'form': form,
                            }, context_instance=RequestContext(request))

def nk_help(request):
    return render_to_response('recipes/contentpage/help.html', { }, context_instance=RequestContext(request))

