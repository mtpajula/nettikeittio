from django.forms import ModelForm
from django.contrib.auth.models import User
from recipes.models import UserProfile
from recipes import models

class UserDataForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
    

class UserProfileRegistrationForm(ModelForm):
    class Meta:
        model = models.UserProfile
        fields = ('name', )
        

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile