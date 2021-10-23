from django import forms
from django.db.models.fields import CharField
from django.forms import fields
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

import account

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='* Add a valid email address')
    class Meta:
        model = models.Account
        fields = ('email','username','password1','password2')
        
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text= ''
        self.fields['password2'].help_text= ''
        self.fields['email'].help_text= ''

class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = models.Account
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Account
        fields = ('email','username')
    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = models.Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except models.Account.DoesNotExist:
                return email

            raise forms.ValidationError('Email "%s" is already in use.'%account.email)
    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = models.Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except models.Account.DoesNotExist:
                return username

            raise forms.ValidationError('Username "%s" is already in use.'%account.username)