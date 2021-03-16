from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.forms import ModelForm
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import ListView

from .forms import (
    HarvestForm,
    LeafForm, 
    PlantForm,
)
from .models.leaf import Leaf
from .models.plant import Plant
from .models.ml import MachineLearning


class LeafCreate(LoginRequiredMixin, CreateView):

    model = Leaf
    form_class = LeafForm
    queryset = Leaf.objects.all()
    template_name = "garden/leaf/create.html"

    def get_context_data(self, plant_id=None, **kwargs):
        """Insert the plant and new leaf into the context dict."""
        context = {}
        if self.object:
            context["object"] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
        context.update(kwargs)
        # adding the plant to the context
        if plant_id is not None:
            context["plant"] = Plant.objects.get(id=plant_id)
        return super().get_context_data(**context)

    def get(self, request: HttpRequest, plant_id: int):
        """Renders the form to check the health of a plant leaf.

        Parameters:
        request(HttpRequest): the GET request sent by the client
        plant_id(int): the unique id of the related Plant instance

        Returns: HttpResponse: the view of the template
        """
        self.object = None
        return self.render_to_response(self.get_context_data(plant_id))

    def diagnose_plant(self, leaf_id):
        """After the new Leaf saves, let the neural network
        diagnose its health.

        Parameter:
        leaf_id(int): unique pk of the Leaf instance

        Returns: HttpResponseRedirect: sends user to view results
        """
        leaf = Leaf.objects.get(id=leaf_id)
        cnn = MachineLearning.objects.get(purpose="V")
        # fill out the fields on the leaf model
        status, condition, confidence = cnn.predict_health(leaf)
        leaf.status = status
        leaf.condition = condition
        leaf.confidence = confidence
        leaf.save()
        # redirect
        return HttpResponseRedirect(self.get_success_url(leaf.plant.id))

    def get_success_url(self, plant_id: int) -> str:
        """TODO: redirect to the LeafDetail, instead of PlantDetail"""
        plant = Plant.objects.get(id=plant_id)
        return plant.get_absolute_url()

    def form_invalid(self, form, plant_id):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(plant_id, form=form))

    def form_valid(self, form, plant_id):
        """Sets the fields on the new Leaf, redirects to see its details."""
        # set the plant attribute of the new leaf
        plant = Plant.objects.get(id=plant_id)
        # fill out the fields on the new Leaf, and save
        form.instance.plant = plant
        form.save()
        # TODO: replace below with super().form_valid(form)
        return self.diagnose_plant(form.instance.id)

    def post(self, request, plant_id):
        """Validates the form submitted by the user, and
        (depending on if the form passes) adds a new Leaf to the db.

        Parameters:
        request(HttpRequest): the GET request sent by the client
        plant_id(int): the unique id of the related Plant instance

        Returns: HttpResponseRedirect: the view of the LeafDetail
        """
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, plant_id)
        return self.form_invalid(form, plant_id)


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

    def form_valid(self, form: ModelForm, request: HttpRequest):
        """Ensures the new Plant instance is connected to the user,
        and that the is_edible field is boolean."""
        form.instance.profile = request.user.profile
        form.instance.is_edible = form.instance.is_edible == True
        return super().form_valid(form)

    def post(self, request: HttpRequest):
        """Submits the new Plant instance to the db, if the form validates."""
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, request)
        return super().form_invalid(form)


class HarvestView(LoginRequiredMixin, TemplateView):
    """User is able to earn points for growing their own produce."""
    
    model = Plant
    form_class = HarvestForm
    template_name = "garden/plant/harvest.html"
    queryset = Plant.objects.filter(is_edible=True)
    success_message = "Huzzah! Congrats, we've lowered your carbon  \
                      footprint in honor of your harvest."

    def get(self, request, slug):
        """Renders the form where users record their harvest.

        Parameters:
        request(HttpRequest): the GET request sent by the client
        slug(str): a unique id of the Plant being harvested

        Returns: HttpResponse: the view of the template with the form

        """
        plant = self.queryset.get(slug=slug)
        form = self.form_class()
        context = {
            "plant": plant,
            "form": form
        }
        return render(request, self.template_name, context)

    def form_valid(self, slug, form) -> HttpResponseRedirect:
        """Updates the database models for the plant and user.

        Parameters:
        slug(str): a unique id of the Plant being harvested
        form(.forms.HarvestForm): holds relevant data about the harvest record

        Returns: HttpResponseRedirect: the player goes back to
                the view of the PlantDetail template

        """
        # A: get the plant and related user
        plant = self.queryset.get(slug=slug)
        user = plant.profile
        # B: get the amount harvested in kg
        new_harvest_amount = form.get_harvest()
        # C: update the plant's total harvest amount and the user's footprint
        plant.amount_harvested_total += new_harvest_amount
        plant.save()
        user.users_footprint -= new_harvest_amount
        user.save()
        # D: redirect to the PlantDetail view    
        return HttpResponseRedirect(plant.get_absolute_url())

    def post(self, request, slug):
        """Processes the form submission and updates the 
        Player and Plant profiles accordingly.

        Parameters:
        request(HttpRequest): the POST request sent by the client
        slug(str): a unique id of the Plant being harvested

        Returns: HttpResponseRedirect: the player goes back to
                the view of the PlantDetail template

        """
        # A: instanitate the form
        form = self.form_class(request.POST)
        # B: validate the form 
        if form.is_valid():
            # add a success message
            messages.add_message(request, messages.SUCCESS, 
                                 self.success_message)
            # process the form as appropiate
            return self.form_valid(slug, form)
        return self.form_invalid(form)



