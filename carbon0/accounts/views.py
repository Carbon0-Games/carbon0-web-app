from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView

from carbon_quiz.models.achievement import Achievement
from .forms import UserSignUpForm
from .models import Profile


# Social Auth
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.views import LoginView
from social_django.models import UserSocialAuth


class UserCreate(SuccessMessageMixin, CreateView):
    '''Display form where user can create a new account.'''
    form_class = UserSignUpForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/auth/signup.html'
    success_message = 'Welcome to Carbon0! You may now log in.'

    def form_valid(self, form, secret_id):
        '''Save the new User, and a new Profile for them, in the database.'''
        self.object = form.save()
        # save a new profile for the user
        profile = Profile.objects.create(user=self.object)
        profile.save()
        # connect this profile to the achievement, if applicable
        if secret_id is not None:
            achievement = Achievement.objects.get(secret_id=secret_id)
            achievement.profile = profile
            achievement.save()
            print('Achievement saved!')
        return super().form_valid(form)

    def post(self, request, secret_id=None):
        """
        Passes the id of the Achievement the profile should include, if any.  

        Parameters:
        request(HttpRequest): the GET request sent to the server
        secret_id(str): unique value on one of the Achievement instances
        
        Returns:
        HttpResponseRedirect: the view of the Login template
        """
        # get form needed for Achievement model instantiation
        form = self.get_form()
        # validate, then create
        if form.is_valid():
            return self.form_valid(form, secret_id)
        # or redirect back to the form
        else:
            return self.form_invalid(form)


# Social Auth
class UserCreateFromSocial(LoginView):
    template_name = 'accounts/auth/signup.html'


class SettingsView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user

        try:
            facebook_login = user.social_auth.get(provider='facebook')
        except UserSocialAuth.DoesNotExist:
            facebook_login = None
        
        try:
            google_login = user.social_auth.get(provider='google-oauth2')
        except UserSocialAuth.DoesNotExist:
            google_login = None

        return render(request, 'accounts/auth/settings.html', {
            'facebook_login': facebook_login,
            'google_login': google_login,
        })


