from django.contrib import admin
from .models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('member', 'type', 'content', 'is_view', 'created')
    list_filter = ('type', 'is_view', 'created')
    list_per_page = 12
    search_fields = ('content',)
    raw_id_fields = ('member',)

admin.site.register(Feedback, FeedbackAdmin)
