from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpRequest
from recipes.models import *

# Simulate slow response from server with time.sleep(2)
# import time

def menu(request):
    return render_to_response('recipes/contentpage/menu.html', { })

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

def search(request, page):
    
    if 'q' in request.GET and request.GET['q']:
        s = request.GET['q']
        
        # Gathering results in results -table
        results = []
        
        r1 = Recipe.objects.all()
        # Filter from recipes only names and descriptions matching search string
        r1 = r1.filter(name__icontains = s) | r1.filter(description__icontains = s)
        results.extend(r1)
        
        #####  ---  This code is for dividing search between pages
        # Give here tha amount of results shown in one page
        results_in_one_page = 10
        
        pages = 1
        pagelist = []
        result_len = len(results)
        
        if result_len >= results_in_one_page and page != "":
            pages = int(result_len / results_in_one_page) + 1
            for i in range(pages):
                pagelist += [i+1]
                
            result_first = (int(page)-1)*results_in_one_page
            result_last = result_first+results_in_one_page
            results = results[result_first:result_last]
            
            page_previous = int(page)-1
            page_next = int(page)+1
            
            if page == '1':
                page_previous = 0
            elif str(page) == str(pages):
                page_next = 0
                
                
            return render_to_response('recipes/contentpage/search.html', 
                { 'results': results,
                   'search_string': s,
                   'pages' : pages,
                   'page_previous' : page_previous,
                   'page_next' : page_next,
                   'pagelist' : pagelist})
        #####  ---  Above code is for dividing search between pages
        
        return render_to_response('recipes/contentpage/search.html',
            { 'results': results,
               'search_string': s })
    
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

