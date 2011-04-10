from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.http import *
from recipes.models import *
import re

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

def search(request):
    return render_to_response('recipes/contentpage/search.html', { })

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

    # Update recipe if post information is received
    if request.method == 'POST':
      return save_edit_recipe(request)
    
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    phases = Phase.objects.all().filter(recipe=recipe_id)

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

