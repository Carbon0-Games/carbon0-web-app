from django.urls import path

from .views import (
    HarvestView,
    LeafCreate,
    PersonalPlantList,
    PlantCreate,
    PlantDelete,
    PlantDetail,
    PlantUpdate,
)


app_name = "garden"

urlpatterns = [
    path("plant/<int:plant_id>/leaf-check/", LeafCreate.as_view(), name="leaf_create"),
    path("plant/<slug:slug>/harvest/", HarvestView.as_view(), name="harvest"),
    path("plant/<slug:slug>/update", PlantUpdate.as_view(), name="plant_update"),
    path("plant/<slug:slug>/delete/", PlantDelete.as_view(), name="plant_delete"),
    path("plant/<slug:slug>/details/", PlantDetail.as_view(), name="plant_detail"),
    path("plant/create/", PlantCreate.as_view(), name="plant_create"),
    path("plant-list/", PersonalPlantList.as_view(), name="plant_list"),
]
