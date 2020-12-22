from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from accounts.models import Profile

# credit for subclassing forms.Form belongs to
# https://overiq.com/django-1-10/django-creating-users-using-usercreationform/


class UserSignUpForm(UserCreationForm):
    """A form that handles registering new users."""

    class Meta:
        model = User
        # fields = ['email', 'username',
        #           'first_name', 'last_name',
        #           'password1', 'password2']
        fields = ["username", "email"]

        def save(self, commit=True):
            """Initializes fields of the new User instance."""
            user = super(User, self).save(commit=False)
            # user.first_name = self.cleaned_data['first_name']
            # user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data["email"]

            if commit is True:
                user.save()

            return user


class ProfileForm(forms.ModelForm):
    """A form for editing accout information."""

    class Meta:
        model = Profile
        fields = [
            "mugshot",
            "phone",
        ]


class DietTrackerForm(forms.ModelForm):
    """
    A form for the player to track how many times 
    they completed the Diet mission.
    """

    class Meta:
        model = Profile
        fields = [
            "diet_sign_photo",
            "photos_are_accurate",
        ]


class TransitTrackerForm(forms.ModelForm):
    """
    A form for the player to track how many times 
    they completed the Transit mission.
    """

    class Meta:
        model = Profile
        fields = [
            "transit_sign_photo",
            "photos_are_accurate",
        ]


class RecyclingTrackerForm(forms.ModelForm):
    """
    A form for the player to track how many times 
    they completed the Recycling mission.
    """

    class Meta:
        model = Profile
        fields = [
            "recycling_sign_photo",
            "photos_are_accurate",
        ]


class OffsetsTrackerForm(forms.ModelForm):
    """
    A form for the player to track how many times 
    they completed the Offsets mission.
    """

    class Meta:
        model = Profile
        fields = [
            "offsets_sign_photo",
            "photos_are_accurate",
        ]


class UtilitiesTrackerForm(forms.ModelForm):
    """
    A form for the player to track how many times 
    they completed the Utilities mission.
    """

    class Meta:
        model = Profile
        fields = [
            "utilities_sign_photo",
            "photos_are_accurate",
        ]
