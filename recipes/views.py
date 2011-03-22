from django.shortcuts import render_to_response, get_object_or_404
from recipes.models import Recipe

def base(request):
    return render_to_response('recipes/base.html', { })

def list(request):
    recipe_list = Recipe.objects.all().order_by('name')
    return render_to_response('recipes/list.html', {'recipe_list': recipe_list, })

def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render_to_response('recipes/detail.html', { 'recipe': recipe })
