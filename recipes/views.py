from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.http import *
from recipes.models import *
import re
from django.http import HttpRequest, HttpResponseRedirect
from recipes.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.template import RequestContext
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.simplejson import *
from django.core import serializers

# Simulate slow response from server with time.sleep(2)
# import time

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
    return render_to_response('recipes/contentpage.html', { }, context_instance=RequestContext(request))

def recipe_search(request):
    return render_to_response('recipes/contentpage/recipe_search_field.html', { }, context_instance=RequestContext(request))

def list_recipes(request):
    
    context = {}
    recipes = Recipe.objects.all()
    
    if 'type' in request.GET and request.GET['type']:
        type = request.GET['type']
        if "n" in type:
            context['results'] = recipes.order_by('-lastedit')
    else:
        context['results'] = recipes.order_by('name')
    return listing(request, context)

def list_users(request):
    context = { 'results': UserProfile.objects.all().order_by('name') }
    return listing(request, context)

# Basic skeleton from http://docs.djangoproject.com/en/dev/topics/pagination/?from=olddocs
def listing(request, context = {}):
    
    results = context['results']
    
    if len(results) != 0:
        paginator = Paginator(results, 5) # Show n contacts per page
        
        getString = ""
        for g, i in request.GET.iteritems():
            if g != 'page':
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
def edit_recipe(request, recipe_id):

    if not request.user.is_authenticated():
        return HttpResponseForbidden

    # Update recipe if post information is received
    if request.method == 'POST':
      return save_edit_recipe(request)
    
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    phases = Phase.objects.all().filter(recipe=recipe_id).order_by('-ordering')

    context = { 'recipe': recipe, 'phases': phases }
    context.update(csrf(request))
    
    return render_to_response('recipes/contentpage/edit_recipe.html', context)

def new_recipe(request):

    if not request.user.is_authenticated():
        return HttpResponseForbidden()


    if request.method == 'POST':
        return save_edit_recipe(request)

    recipe = Recipe(
        owner=request.user.get_profile(),
        name='',
        description='',
        image='',
        editable=0,
        eddits=0,
        lastedit=datetime.date.today()
    )
    recipe.save();
    # No phases created yet
    phases = Phase.objects.none()

    context = { 'recipe': recipe, 'phases': phases }
    context.update(csrf(request))
    
    return render_to_response('recipes/contentpage/edit_recipe.html', context)

#
# Save recipe with parameters specified in POST. Called from edit_recipe
#
def save_edit_recipe(request):
    if request.method != 'POST':
        return HttpResponseBadRequest

    print request.POST

    #Replace non-digits
    re_numeric = re.compile('[^0-9]' )
    r_id = request.POST['recipe_id']
    re_numeric.sub('', r_id)
    rec = Recipe.objects.get(pk=r_id)

    rec.name = request.POST['recipe_name']
    rec.description = request.POST['recipe_description']

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
    Phase.objects.filter(recipe=r_id).select_related('phase').delete()
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

                # TODO: Should check for existence first
                ing = Ingredient(
                    name=i_name
                )
                ing.full_clean()
                ing.save()

                # TODO: Should check for existence first
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
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


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
    results = []
    if request.method == "GET":
        if request.GET.has_key(u'term'):
            value = request.GET[u'term']
            # Ignore queries shorter than length 2
            if len(value) > 1:
                result = []
                model_results = Ingredient.objects.filter(name__icontains=value)
                #results = [ x.name for x in model_results ]
                #results = [ (x.__unicode__(), x.id) for x in model_results ]
                #results = [ (x.name, x.id) for x in model_results ]
                #result = serializers.serialize('json', model_results)
                for x in model_results:
                    d = { 'id': x.id, 'name': x.name }
                    #result.extend((x.name, str(x.id)) for x in model_results)
                    result.extend(str(d))
                #print result
                    #result += x.name + "|" + str(x.id) + "\n"
                #result = serializers.serialize('json', result)
                #result = '[{"pk":"1","name":"oliivi"},{"pk":"2","name":"oliivioljy"},{"pk":"3","name":"oli"}]'
            else:
                result = ""
    
    print result
    json = simplejson.dumps(result)
    print json
    
    return HttpResponse(json)

