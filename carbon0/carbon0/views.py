from django.shortcuts import render


def get_landing(request):
    '''Render the landing page of the site.'''
    return render(request, "index.html")