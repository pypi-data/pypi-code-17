from django.contrib import admin

from .models import categoryItem
from .models import siteMainInfo
from .models import siteSocialMediaReference
from .models import contentArticle
from .models import itemLayout
from .models import theme

# Register your models here.

admin.site.register(categoryItem)
admin.site.register(siteMainInfo)
admin.site.register(siteSocialMediaReference)
admin.site.register(contentArticle)
admin.site.register(itemLayout)
admin.site.register(theme)
