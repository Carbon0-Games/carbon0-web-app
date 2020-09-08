from django.shortcuts import render


def get_landing(request):
    '''Returns the view for the landing page template.'''
    return render(request, "index.html")