from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView

from .forms import UserSignUpForm
from .models import Profile


# Social Auth
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from social_django.models import UserSocialAuth


class UserCreate(SuccessMessageMixin, CreateView):
    '''Display form where user can create a new account.'''
    form_class = UserSignUpForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/auth/signup.html'
    success_message = 'Welcome to Carbon0! You may now log in.'

    def form_valid(self, form):
        '''Save the new User, and a new Profile for them, in the database.'''
        self.object = form.save()
        profile = Profile.objects.create(user=self.object)
        profile.save()
        return super().form_valid(form)





# Home View Social Auth
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"


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

        can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

        return render(request, 'accounts/auth/settings.html', {
            'facebook_login': facebook_login,
            'google_login': google_login,
            'can_disconnect': can_disconnect
        })


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:settings')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'accounts/auth/password.html', {'form': form})