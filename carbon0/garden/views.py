from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.views.generic.detail import DetailView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import ListView

from .forms import LeafForm, PlantForm
from .models.leaf import Leaf
from .models.plant import Plant


class LeafCreate(LoginRequiredMixin, CreateView):

    model = Leaf
    form_class = LeafForm
    queryset = Leaf.objects.all()
    template_name = "garden/leaf/create.html"

    def get(self, request, plant_id):
        # add the plant to the context
        pass
    
    def form_valid(form, plant_id):
        pass

    def post(self, request, plant_id):
        pass

    
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
        context = {"plant": plant, "plant_leaves": leaves}
        # return the response
        return render(request, self.template_name, context)


class PlantCreate(LoginRequiredMixin, CreateView):
    """A view for the user to register plants."""

    model = Plant
    form_class = PlantForm
    template_name = "garden/plant/create.html"
    queryset = Plant.objects.all()

    def get(self, request):
        """Returns a form the user can use to add a new Plant."""
        return render(request, self.template_name)

    def form_valid(self, form: ModelForm, request: HttpRequest):
        """Ensures the new Plant instance is connected to the user."""
        form.instance.profile = request.user.profile
        return super().form_valid(form)

    def post(self, request: HttpRequest):
        """Submits the new Plant instance to the db, if the form validates."""
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, request)
        return super().form_invalid(form)
