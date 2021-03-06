from django import forms
from rango.models import Page, Category, UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=Category.NAME_MAX_LENGTH, help_text="Please enter the category name.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	#Inline class provides additional info on form.
	class Meta:
		#Provide association between ModelForm and model
		model = Category
		fields = ('name',)

class PageForm(forms.ModelForm):
	title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH, help_text="Please enter the title of the page.")
	url = forms.URLField(max_length=Page.URL_MAX_LENGTH, help_text="Please enter the URL of the page.")		
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	class Meta:
		#Provide association between the ModelForm and a model
		model = Page

		#What fields do we want to include?
		#This way we don't need every field in model present.
		#Some fields may allow null values as we might not want to include them
		#Here we're hiding foreign key, we can either exclude category field from form:
		exclude = ('category',)
		#or specify fields to include without category...
		#fields = ('title', 'url', 'views')

	def clean(self):
		cleaned_data = self.cleaned_data
		url = cleaned_data.get('url')

		#If url not empty and doesn't start with 'http://' then prepend it
		if url and not url.startswith('http://'):
			url = f'http://{url}'
			cleaned_data['url'] = url
		
		return cleaned_data

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('website', 'picture',)