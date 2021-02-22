from django.urls import path
from .views import (
    PlantDetail,
    PersonalPlantList,
)


app_name = "garden"

urlpatterns = [
    path("plant/<slug:slug>/", PlantDetail.as_view(), name="plant_detail"),
    path("plant-list/", PersonalPlantList.as_view(), name="plant_list"),
]
