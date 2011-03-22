from django.db import models
from django.contrib.auth.models import User # Link UserProfiles to auth Users

# Recipes user profile
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    name = models.CharField('User name', max_length=50)
    description = models.TextField('User description', max_length=1000)
    image = models.ImageField(upload_to='user_images')
    favorites = models.ManyToManyField("Recipe", blank=True, null=True)
    
    def __unicode__(self):
        return 'UserProfile: ' + self.name

# Automatically create UserProfile when needed (User registers)
# http://www.turnkeylinux.org/blog/django-profile
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0]);

# Main recipe
class Recipe(models.Model):
    owner = models.ForeignKey(UserProfile)
    name = models.CharField('Recipe full name', max_length=200)
    description = models.TextField('Recipe description', max_length=1000)
    image = models.ImageField(upload_to='recipe_images/%Y/%m/%d', blank=True, null=True)
    editable = models.IntegerField('Editing allowed')
    eddits = models.IntegerField('Number of times edited')
    lastedit = models.DateTimeField('Last edit date')

    tags = models.ManyToManyField('Tag', blank=True, null=True)
    
    def __unicode__(self):
        return 'Recipe: ' + self.name + ' by ' + self.owner.name    
    
# Recipe phases
class Phase(models.Model):
    name = models.CharField('Phase name', max_length=200)
    description = models.TextField('Phase description', max_length=1000)
    activity_type = models.IntegerField('Activity type (passive/active)')
    duration_min = models.IntegerField('Phase duration in minutes')
    ordering = models.IntegerField('Phase position in recipe')
    recipe = models.ForeignKey(Recipe)

    def __unicode__(self):
        return 'Phase: ' + self.name + ' of ' + self.recipe.name 

class Unit(models.Model):
    name = models.CharField('Unit name', max_length=50)
    description = models.CharField('Unit description', max_length=200)
    
    def __unicode__(self):
        return 'Unit: ' + self.name

class Ingredient(models.Model):
    name = models.CharField('Ingredient name', max_length=50)

    def __unicode__(self):
        return 'Ingredient: ' + self.name

class PhaseIngredient(models.Model):
    phase = models.ForeignKey(Phase)
    ingredient = models.ForeignKey(Ingredient)
    unit = models.ForeignKey(Unit)
    amount = models.DecimalField(max_digits=5, decimal_places=2)

    def __unicode__(self):
        return 'PhaseIngredient: ' + self.ingredient.name + ' in ' + self.phase.name


# Tags
class Tag(models.Model):
    name = models.CharField('Tag name', max_length=30)
    
    def __unicode__(self):
        return 'Tag: ' + self.name

class Comment(models.Model):
    user = models.ForeignKey(UserProfile)
    recipe = models.ForeignKey(Recipe)
    title = models.CharField('Comment title', max_length=50)
    text = models.TextField('Comment content', max_length=2000)
    added = models.DateTimeField('Comment date')
    image = models.ImageField(upload_to='comment_images/%Y/%m/%d')
    rating = models.IntegerField()
    
    def __unicode__(self):
        return 'Comment: ' + user.name + ' about ' + self.recipe.name + ': ' + self.title + ' - ' + self.text
