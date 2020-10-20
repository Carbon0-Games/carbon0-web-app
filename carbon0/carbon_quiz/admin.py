from django.contrib import admin

from .models.link import Link
from .models.question import Question
from .models.mission import Mission
from .models.quiz import Quiz
from .models.achievement import Achievement


# Make ModelAdmins
class LinkInline(admin.StackedInline):
    model = Link
    extra = 3


class MissionAdmin(admin.ModelAdmin):
    fieldsets = [
    (None, {'fields': [
        'title',
        'action',
        'clicks_needed',
        'learn_more',
        'question',
        'percent_carbon_sequestration',
    ]}),
    ]
    inlines = [LinkInline]



# Register your models here
admin.site.register(Link)
admin.site.register(Question)
admin.site.register(Mission, MissionAdmin)
admin.site.register(Quiz)
admin.site.register(Achievement)

# Custom header for the Admin Site
admin.site.site_header = "Carbon0 Games Administration"
