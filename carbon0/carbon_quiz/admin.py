from django.contrib import admin
from .models import (
    Question,
    Mission,
    Quiz,
    Achievement,
)


# Register your models here
admin.site.register(Question)
admin.site.register(Mission)
admin.site.register(Quiz)
admin.site.register(Achievement)
