from django.conf import settings
from django.shortcuts import render


def get_landing(request):
    '''Render the landing page of the site.'''
    # set the context of the view
    context = {
        'MIXPANEL_TOKEN': settings.MIXPANEL_TOKEN
    }
    # return the response
    return render(request, "index.html", context)