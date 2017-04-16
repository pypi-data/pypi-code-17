from django.conf.urls import url

from omCmsMain.views import baseIndex, categoryArticleDetail

urlpatterns = [
    url(r'^$', baseIndex),
    url(r'^(?P<category>\w+)/(?P<article_id>\w+)/$', categoryArticleDetail),
] 
