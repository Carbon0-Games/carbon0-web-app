from django.urls import path
from .views import (
    PlantDetail,
    PlantList,
)


app_name = "garden"

urlpatterns = [
    path("plant/<slug:nickname>/", PlantDetail.as_view(), 
         name="plant_detail"),
    path("plant-list/", PlantList.as_view(), name="plant_list"),
]
