from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from django.views.static import serve

from .models.leaf import Leaf
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
]

# in development, let Django serve leaf images:
if settings.DEBUG is True:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': Leaf.UPLOAD_LOCATION
        }),
    ]
