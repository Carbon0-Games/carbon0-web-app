from django.urls import path
from .views import (
    PlantList,
)


app_name = "garden"

urlpatterns = [
    path("plant-list/", PlantList.as_view(), name="plant_list"),
]
