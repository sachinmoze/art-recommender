from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, UserInteraction
from recommendations.models import Preference

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    preferences = forms.ModelMultipleChoiceField(
        queryset=Preference.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text='Select your preferences.'
    )

    class Meta:
        model = UserProfile
        fields = ['preferences']

class UserInteractionForm(forms.ModelForm):
    interaction_type = forms.ChoiceField(choices=[
        ('view', 'View'),
        ('like', 'Like'),
        ('share', 'Share'),
    ], help_text='Select the type of interaction.')

    class Meta:
        model = UserInteraction
        fields = ['artwork', 'interaction_type']
