from django import forms
from restaurants.models import RestaurantLocation, Author, Book
from .validators import validate_category

class RestaurantCreateForm(forms.Form):
	name		= forms.CharField(label="Rest Name")
	location	= forms.CharField(required=False)
	category	= forms.CharField(required=False)

	def clean_name(self):
		name = self.cleaned_data.get('name')
		if name == 'Hello':
			raise forms.ValidationError(
				('Invalid value: %(value)s'),
    				params={'value': name},
				)
		return name

class RestaurantLocationCreateForm(forms.ModelForm):
	# email		= forms.EmailField()
	# category = forms.CharField(required=False, validators=[validate_category])
	class Meta:
		model = RestaurantLocation
		fields = [
			'name',
			'location',
			'category',
		]

	def clean_name(self):
		name = self.cleaned_data.get('name')
		if name == 'create':
			raise forms.ValidationError('Invalid value: %(value)s',
    				params={'value': name},
				)
		return name

	# def clean_email(self):
	# 	email = self.cleaned_data.get('email')
	# 	if ".edu" in email:
	# 		raise forms.ValidationError('We do not accept : %(value)s',
 #    				params={'value': '.edu'},
	# 			)
	# 	return email
