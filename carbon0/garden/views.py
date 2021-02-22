from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from .models.plant import Plant


class PlantList(ListView):

    model = Plant
    queryset = Plant.objects.all()
    template_name = "garden/plant/list.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """Where the user can see all their registered plants.
        
        Parameters:
        request(HttpRequest): the GET request sent by the client

        Response: HttpResponse: the view of the template
        """
        # define the context
        context = {"plants": self.get_queryset()}
        # return the response
        return render(request, self.template_name, context)
