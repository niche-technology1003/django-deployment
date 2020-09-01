from django import forms
from django.core import validators
from .models import Topic, UserProfileInfo
from django.contrib.auth.models import User


# keyword "value" is mandatory
def name_validations(value):
    if value[0].lower() != 'a':
        raise validators.ValidationError("Name must start with A(a)")


class FormName(forms.Form):
    # custom validations
    name = forms.CharField(validators=[name_validations])
    # inbuilt validations
    email = forms.EmailField(validators=[validators.MaxLengthValidator(15)])
    verify_email = forms.EmailField()
    text = forms.CharField(widget=forms.Textarea)

    # if you define a method as clean_name, django will automatically know that its a clean method for attribute "name"
    # single clean is for all field at once
    def clean(self):
        clean_all_fields = super().clean()
        email = clean_all_fields['email']
        vmail = clean_all_fields['verify_email']

        if email != vmail:
            raise forms.ValidationError("emails are not matching")


class TopicForm(forms.ModelForm):
    # Add validations here
    # and additional fields
    class Meta:
        # This must be always called "model"
        model = Topic
        fields = "__all__"


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ('profile_site', 'profile_picture')
