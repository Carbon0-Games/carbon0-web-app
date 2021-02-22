from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import ListView

from .models.leaf import Leaf
from .models.plant import Plant


class PersonalPlantList(LoginRequiredMixin, ListView):

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


class PlantDetail(LoginRequiredMixin, DetailView):
    """Displays the details and leaves related a certain plant."""
    
    model = Plant
    template_name = "garden/plant/detail.html"

    def get(self, request, slug):
        """Renders the view of the Plant and its leaves.

        Parameters:
        request(HttpRequest): the GET request made by the client
        slug(str): the unique slug of a specific Plant instance

        Returns:
        HttpResponse: the view of the template
        """
        # get the Plant object via the slug
        plant = Plant.objects.get(slug=slug)
        # get the related leaves, sorted by date added
        leaves = Leaf.objects.filter(plant=plant)
        # define the context
        context = {
            "plant": plant,
            "plant_leaves": leaves
        }
        # return the response
        return render(request, self.template_name, context)


class PlantCreate(CreateView):
    """A view for the user to register plants."""
    pass