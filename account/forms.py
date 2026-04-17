from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

class CreateCustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2',]

    def __init__(self, *args, **kwargs):
        super(CreateCustomUserForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is in our database already!')
        if len(email) >= 350:
            raise forms.ValidationError('Your email address is too long!')
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

class UpdateUserForm(forms.ModelForm):

    password = None


    class Meta:
        model = CustomUser
        fields = ['username', 'email']
        exclude = ['password1', 'password1']

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        # Mark email as required

        self.fields['email'].required = True

        
    # Email validation
    
    def clean_email(self):

        email = self.cleaned_data.get("email")

        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():

            raise forms.ValidationError('This email is invalid')

        # len function updated ###

        if len(email) >= 350:

            raise forms.ValidationError("Your email is too long")


        return email








