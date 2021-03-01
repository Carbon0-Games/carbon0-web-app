from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    LeafCreate,
    PlantCreate,
    PlantDetail,
    PersonalPlantList,
)


app_name = "garden"

urlpatterns = [
    path("plant/<int:plant_id>/leaf-check/", LeafCreate.as_view(), name="leaf_create"),
    path("plant/details/<slug:slug>/", PlantDetail.as_view(), name="plant_detail"),
    path("plant/create/", PlantCreate.as_view(), name="plant_create"),
    path("plant-list/", PersonalPlantList.as_view(), name="plant_list"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
