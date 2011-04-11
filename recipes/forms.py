from django.forms import ModelForm
from django.contrib.auth.models import User
from recipes.models import UserProfile

class UserDataForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
    

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile