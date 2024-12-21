# forms.py
from django import forms
from store_app.models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['firstname', 'lastname', 'phone', 'address', 'city', 'state', 'country', 'postcode', 'email']
