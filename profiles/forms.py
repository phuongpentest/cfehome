from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

User = get_user_model()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2',
              )

    def clean_email(self):
      email = self.cleaned_data.get('email')
      # email = super().clean_email()
      qs = User.objects.filter(email__iexact=email)
      if qs.exists():
        raise forms.ValidationError("Can not use this email. It's already used")
      return email        

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.is_active = False

        if commit:
            user.save()
            # print(user.profile)
            user.profile.send_activation_email()
        return user

class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
        )
