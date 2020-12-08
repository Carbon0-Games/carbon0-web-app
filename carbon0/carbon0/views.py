from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import reverse


def get_landing(request):
    """Render the landing page of the site, or redirect to the profile."""
    # if the user is logged in
    if request.user.is_authenticated:
        # redirect to the user's profile page
        return HttpResponseRedirect(reverse("accounts:profile"))
    # set the context of the view
    context = {"app_id": settings.FACEBOOK_SHARING_APP_ID}
    try:  # track using Mixpanel in production only
        context["MP_PROJECT_TOKEN"] = settings.MP_PROJECT_TOKEN
    except AttributeError:
        pass
    # return the response
    return render(request, "index.html", context)
