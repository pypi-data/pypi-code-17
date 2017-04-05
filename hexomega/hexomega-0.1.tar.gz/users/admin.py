from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(AdminUser)
admin.site.register(LeaderUser)
admin.site.register(Role)
admin.site.register(ActionList)
admin.site.register(Task)
admin.site.register(ActivityLog)
admin.site.register(Project)
admin.site.register(MemberUser)
