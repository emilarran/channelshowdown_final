from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )

        def save(self, commit=True):
            user = super(RegistrationForm, self).save(commit=False)
            user.email = self.cleaned_data['email']

            if commit:
                user.save()

            return user


class EditUserForm(forms.Form):
    username = forms.CharField()
    bio = forms.CharField()
    firstName = forms.CharField()
    lastName = forms.CharField()

    def save(self, *args, **kwargs):
        username = self.cleaned_data['username']
        user = User.objects.get(username=username)
        first_name = self.cleaned_data['firstName']
        last_name = self.cleaned_data['lastName']
        bio = self.cleaned_data['bio']
        user.first_name = first_name
        user.last_name = last_name
        user.userinfo.bio = bio
        user.save()
        user.userinfo.save()
