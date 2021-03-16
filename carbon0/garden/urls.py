from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from django.views.static import serve

from .models.leaf import Leaf
from .views import (
    HarvestView,
    LeafCreate,
    PlantCreate,
    PlantDetail,
    PersonalPlantList,
)


app_name = "garden"

urlpatterns = [
    path("plant/<int:plant_id>/leaf-check/", LeafCreate.as_view(), name="leaf_create"),
    path("plant/details/<slug:slug>/harvest/", HarvestView.as_view(),
         name="harvest"),
    path("plant/details/<slug:slug>/", PlantDetail.as_view(), name="plant_detail"),
    path("plant/create/", PlantCreate.as_view(), name="plant_create"),
    path("plant-list/", PersonalPlantList.as_view(), name="plant_list"),
]
