from django.contrib import admin

from .models.question import Question
from .models.mission import Mission
from .models.quiz import Quiz
from .models.achievement import Achievement

# Register your models here
admin.site.register(Question)
admin.site.register(Mission)
admin.site.register(Quiz)
admin.site.register(Achievement)

# Custom header for the Admin Site
admin.site.site_header = 'Carbon0 Games Administration'
