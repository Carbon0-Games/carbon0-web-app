from django.conf import settings
from django.shortcuts import render


def get_landing(request):
    """Render the landing page of the site."""
    # set the context of the view
    context = {"app_id": settings.FACEBOOK_SHARING_APP_ID}
    try:  # track using Mixpanel in production only
        context["MP_PROJECT_TOKEN"] = settings.MP_PROJECT_TOKEN
    except AttributeError:
        pass
    # return the response
    return render(request, "index.html", context)
