from .models import UserPr
from django.contrib.auth.models import User
from django.forms import ModelForm 
from django import forms

class RegForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    check_password = forms.CharField(label = 'Verify', widget=forms.PasswordInput())

    
    class Meta:
        model = UserPr
        exclude = ('user',)
  
    def clean_username(self):
        
        cleaned_data = super(RegForm,self).clean()
        username = cleaned_data.get('username')
        try:
            User.objects.get(username = cleaned_data['username'])
        except User.DoesNotExist:
            return cleaned_data['username']
        raise forms.ValidationError("there is an account with this username")
    
   
    def clean(self):
        cleaned_data=super(RegForm, self).clean()
        password = cleaned_data.get('password')
        check_password = cleaned_data.get('check_password')
        if password != check_password:
            raise forms.ValidationError("the passwords dont match")
        return cleaned_data
    
class LoginForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = UserPr
        fields = ['email','password',]