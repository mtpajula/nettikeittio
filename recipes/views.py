# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.http import *
from recipes.models import *
import re
from django.http import HttpRequest, HttpResponseRedirect
from recipes.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.template import RequestContext

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Used for serializing responses for autocomplete
from django.utils.simplejson import *

from django.core import serializers

# Used for getting current time
from time import strftime



def menu(request):
    if request.user.is_authenticated():
        print "user"
    return render_to_response('recipes/contentpage/menu.html', { }, context_instance=RequestContext(request))

def render_detail_recipe(request, recipe_id, recipe_template):
    
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    phase_list = Phase.objects.filter(recipe = recipe).order_by('ordering')
    ingredient_list = PhaseIngredient.objects.filter(phase__recipe = recipe)
    
    return render_to_response(recipe_template, {
                                'recipe': recipe,
                                'phase_list': phase_list,
                                'ingredient_list': ingredient_list }, context_instance=RequestContext(request))

def main_page(request):

    recipes = Recipe.objects.order_by('lastedit')[:10]

    users = UserProfile.objects.order_by('?')[:10]

    return render_to_response('recipes/contentpage/frontpage.html', { 'recipes': recipes, 'users': users }, context_instance=RequestContext(request))






def recipe_search(request):
    return render_to_response('recipes/contentpage/recipe_search_field.html', { }, context_instance=RequestContext(request))

def own_recipes(request):
    context = {}
    if not request.user.is_authenticated():
        return HttpResponseForbidden

    recipes = Recipe.objects.filter(owner = request.user.get_profile())
    
    context['search_description'] = 'Omat reseptit'
    context['DOM_class_string'] = 'ownColor'
    context['results'] = recipes
    
    return listing(request, context)
    
def favourite_recipes(request):
    context = {}
    if not request.user.is_authenticated():
        return HttpResponseForbidden
    
    nk_user = UserProfile.objects.get(user = request.user.get_profile())

    favorites = nk_user.favorites.all()
    
    context['search_description'] = 'Omat suosikkireseptit'
    context['DOM_class_string'] = 'ownColor'
    context['results'] = favorites
    return listing(request, context)

def list_recipes(request):
    
    results = []
    context = {}
    recipes = Recipe.objects.all()
    
    if 'type' in request.GET and request.GET['type']:
        type = request.GET['type']
        if "n" in type:
            context['results'] = recipes.order_by('-lastedit')
            context['search_description'] = 'Uusimmat reseptit'
    else:
        context['results'] = recipes.order_by('name')
        context['search_description'] = 'Kaikki reseptit'
    
    
    if 'i' in request.GET and request.GET['i']:
        i_list = request.GET.getlist('i')

        id_listlist = []
        
        # Getting all recipe id's that have one of the queryed ingredients in it
        for i in i_list:
            id_list = []
            pi = PhaseIngredient.objects.filter(ingredient__name__icontains=i)
            for item in pi:
                id_list.append(item.phase.recipe.id)
            
            id_listlist.append(id_list)

        # Filtering recipes including all listed ingredients with id list
        r_results = Recipe.objects.none()
        f = True
        for r in id_listlist:
            if f == True:
                r_results = Recipe.objects.filter(id__in=r)
                f = False
            else:
                r_results = r_results.filter(id__in=r)

        context['search_description'] = 'Raaka-ainehaulla'
        context['results'] = r_results
    
    
    return listing(request, context)

def list_users(request):
    context = {}
    context['results'] = UserProfile.objects.all().order_by('name')
    context['search_description'] = 'Kaikki käyttäjät'
    return listing(request, context)

# Basic skeleton from http://docs.djangoproject.com/en/dev/topics/pagination/?from=olddocs
def listing(request, context = {}):
    
    results = context['results']
    
    if len(results) != 0:
        paginator = Paginator(results, 5) # Show n contacts per page
        
        getString = ""
        for g, i in request.GET.iteritems():
            if g == 'page':
                pass
            elif g == 'i':
                i_list = request.GET.getlist('i')
                for ingr in i_list:
                    getString += "&i="+ingr
            else:
                getString += "&%s=%s" % (g, i)
                
        context['getString'] = getString
        
        if 'page' in request.GET and request.GET['page']:
            
            page = request.GET.get('page')
            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                results = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                results = paginator.page(paginator.num_pages)
        else:
            results = paginator.page(1)
            
        context['results'] = results
    else:
        del context['results']
    
    return render_to_response('recipes/contentpage/listing.html', context, context_instance=RequestContext(request))

def search(request):
    # Gathering results in results -table
    results = []
    context = {}
                
    if 'q' in request.GET and request.GET['q']:
        s = request.GET['q']
        
        r1 = Recipe.objects.all()
        # Filter from recipes only names and descriptions matching search string
        r1 = r1.filter(name__icontains = s) | r1.filter(description__icontains = s)
        results.extend(r1)
        
        r2 = UserProfile.objects.all()
        # Filter from recipes only names and descriptions matching search string
        r2 = r2.filter(name__icontains = s) | r2.filter(description__icontains = s)
        results.extend(r2)
        
        context['search_string'] = s
        
    context['results'] = results
    return listing(request, context)

def recipe_detail(request, recipe_id):    
    return render_detail_recipe(request, recipe_id, 'recipes/contentpage/detail.html')

def active(request, recipe_id):
    #recipe = get_object_or_404(Recipe, pk=recipe_id)
    #return render_to_response('recipes/fullpage.html', { 'recipe': recipe })
    return render_detail_recipe(request, recipe_id, 'recipes/fullpage.html')



#
# Edits recipe if data is posted and displays recipe edit form
#
@login_required
def edit_recipe(request, recipe_id):

    #if not request.user.is_authenticated():
    #    return HttpResponseForbidden

    # Update recipe if post information is received
    if request.method == 'POST':
      return save_edit_recipe(request)
    
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    phases = Phase.objects.all().filter(recipe=recipe_id).order_by('ordering')

    context = { 'recipe': recipe, 'phases': phases }
    context.update(csrf(request))

    
    return render_to_response('recipes/contentpage/edit_recipe.html', context, context_instance=RequestContext(request))

def new_recipe(request):

    if not request.user.is_authenticated():
        return HttpResponseForbidden()


    if request.method == 'POST':
        return save_edit_recipe(request)

    # Create empty recipe and phase set
    recipe = Recipe(pk=0,name='',description='')
    phases = Phase.objects.none()

    context = { 'recipe': recipe, 'phases': phases }

    context.update(csrf(request))
    
    return render_to_response('recipes/contentpage/edit_recipe.html', context, context_instance=RequestContext(request))

#
# Save recipe with parameters specified in POST. Called from edit_recipe
#
def save_edit_recipe(request):
    if request.method != 'POST':
        return HttpResponseBadRequest


    #Replace non-digits
    re_numeric = re.compile('[^0-9]' )
    r_id = request.POST['recipe_id']
    re_numeric.sub('', r_id)
    if r_id < 1:
      r_id = 0

    try:
      rec = Recipe.objects.get(pk=r_id)
      # If recipe found, check it's owner and editability
      if rec.editable == 0:
        if rec.owner == request.user.id:
          return HttpResponseForbidden()

    except:
      rec = Recipe()
      rec.eddits = 0

    rec.name = request.POST['recipe_name']
    rec.description = request.POST['recipe_description']
    rec.owner = UserProfile.objects.get(pk=request.user.id)
    rec.eddits = rec.eddits + 1
    rec.lastedit = strftime("%Y-%m-%d %H:%M:%S")

    editable = request.POST['recipe_editable']
    re_numeric.sub('', editable)
    rec.editable = editable

    # Replace invalid chars
    rec.full_clean()
    rec.save()

    phases = { }

    reg_phase = re.compile('phase_([0-9]+)_([a-z]*)_*([0-9]*)_*([a-z_]*)')

    # Parse post variables into dictionary object in form:
    # phases: contains phase ordering numbers
    # phases[num]: contains phase parameters (name, descr, etc)
    # phases[num]["ingredients"] contains each ingredient
    # phases[num]["ingredients"][ingnum] contains params for the ingredient (name, amount, unit)
    for key, value in request.POST.iteritems():
        match = reg_phase.match(key)
        phasenum = -1
        try:
            phasenum = int(match.group(1))
        except:
            continue # No phase num found -> no phase information

        if not phasenum in phases:
            phases[phasenum] = { }

        phaseparam = match.group(2)

        ingnum = -1
        ingparam = ''
        if phaseparam == 'ingredient':
            if not 'ingredients' in phases[phasenum]:
                phases[phasenum]['ingredients'] = { }

            try:
                ingnum = int(match.group(3))
            except:
                continue # Invalid ingredient index

            ingparam = match.group(4)

            if not ingnum in phases[phasenum]['ingredients']:
                phases[phasenum]['ingredients'][ingnum] = { }

            phases[phasenum]['ingredients'][ingnum][ingparam] = value

        else:
            phases[phasenum][phaseparam] = value

    # Delete existing phase and phaseingredient objects bound to current recipe
    Phase.objects.filter(recipe=r_id).select_related('phaseingredient').delete()
    Phase.objects.filter(recipe=r_id).delete()
    for phase, dic in phases.iteritems():

        # Ensure that no empty values are passed to integer fields
        for param, value in phases[phase].iteritems():
            if value in('ordering', 'act', 'duration'):
                phases[phase][param] = re_numeric.sub('', value)
                if phases[phase][param] == '':
                    phases[phase][param] = 0
        
        # First try to find phase having foreign key to current recipe
        # and same ordering number as this one
        p = Phase(
            name=phases[phase]['name'],
            description=phases[phase]['descr'],
            ordering=phases[phase]['ordering'],
            activity_type=phases[phase]['act'],
            duration_min=phases[phase]['duration'],
            recipe=rec
        )
        p.full_clean()
        p.save()
        

        # Loop through each ingredient and its parameters
        if 'ingredients' in phases[phase]:
            for ingnum, params in phases[phase]['ingredients'].iteritems():
                i_name = params['name']
                i_unit= params['unit']
                i_amount = params['amount']

                try:
                    ing = Ingredient.objects.filter(name=i_name)[:1][0]
                except IndexError:
                    ing = Ingredient(
                        name=i_name
                    )
                    ing.full_clean()
                    ing.save()


                try:
                    un = Unit.objects.filter(name=i_unit)[:1][0]
                except IndexError:
                    un = Unit(
                        name=i_unit,
                        description=i_unit
                    )
                    un.full_clean()
                    un.save()           

                pi = PhaseIngredient(
                    phase=p,
                    ingredient=ing,
                    unit=un,
                    amount=i_amount
                )
                pi.full_clean()
                pi.save()       


    # Return redirect to avoid reposting information on page refreshh
    context = { 'recipe': rec }
    context.update(csrf(request))
    
    return render_to_response('recipes/contentpage/edit_recipe.html', context, context_instance=RequestContext(request))


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

def ingredient_lookup(request):

    if request.method == "GET":
        if request.GET.has_key(u'term'):
            value = request.GET[u'term']
            # Ignore queries shorter than length 2
            if len(value) > 1:
                result = []
                model_results = Ingredient.objects.filter(name__icontains=value)
                for x in model_results:
                    result.append({"id":x.id, "name":x.name})
            else:
                result = ""

    json = simplejson.dumps(result)
    return HttpResponse(
        json,
        content_type = 'application/javascript; charset=utf8'
    )

def unit_lookup(request):

    if request.method == "GET":
        if request.GET.has_key(u'term'):
            value = request.GET[u'term']
            # Ignore queries shorter than length 2
            if len(value) > 1:
                result = []
                model_results = Unit.objects.filter(name__icontains=value)
                for x in model_results:
                    result.append({"id":x.id, "name":x.name})
            else:
                result = ""

    json = simplejson.dumps(result)
    return HttpResponse(
        json,
        content_type = 'application/javascript; charset=utf8'
    )

