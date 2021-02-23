from django.contrib import admin

from .models.leaf import Leaf
from .models.plant import Plant
from .models.ml import MachineLearning


admin.site.register(Leaf)
admin.site.register(Plant)
admin.site.register(MachineLearning)
