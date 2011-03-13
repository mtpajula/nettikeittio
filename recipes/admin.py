from django.contrib import admin

from recipes.models import UserProfile, Recipe, Phase, Unit, Ingredient, PhaseIngredient, Tag, Comment


admin.site.register([UserProfile, Recipe, Phase, Unit, Ingredient, PhaseIngredient, Tag, Comment])
