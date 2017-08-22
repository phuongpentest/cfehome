from django.core.exceptions import ValidationError

def validate_even(value):
    if value % 2 != 0:
        raise ValidationError('%(value)s is not an even number',
            params={'value': value},
        )

def validate_email(value):
		email = value
		if ".edu" in email:
			raise forms.ValidationError('We do not accept : %(value)s',
    				params={'value': '.edu'},
				)

CATEGORIES = ['Mexican', 'Asian', 'American', 'Whatever']

def validate_category(value):
	cat = value.capitalize()
	if not cat in CATEGORIES:
		raise ValidationError("%(value)s not a valid category", params={'value': value})
