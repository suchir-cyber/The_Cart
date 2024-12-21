from django import forms
from django.contrib.auth.models import User
from store_app.models import Profile

class ProfileUpdateForm(forms.ModelForm):
    # Add user-related fields
    username = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ['firstname', 'lastname', 'phone', 'address', 'city', 'state', 'country', 'postcode', 'email']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].initial = self.instance.user.username  # Set the initial value to the current username
        self.fields['email'].initial = self.instance.user.email  # Set the initial value to the current email

    def save(self, commit=True):
        profile = super().save(commit=False)  # Save the profile model instance
        user = self.instance.user  # Get the associated user

        # Update the user model fields
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()  # Save the user instance
            profile.save()  # Save the profile instance

        return profile
