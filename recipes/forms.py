from django.forms import ModelForm
from django.contrib.auth.models import User
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
        model = models.UserProfile
        fields = ('name', 'description', 'image')
        
class CommentForm(ModelForm):
    class Meta:
        model = models.Comment
        fields = ('title', 'text')

