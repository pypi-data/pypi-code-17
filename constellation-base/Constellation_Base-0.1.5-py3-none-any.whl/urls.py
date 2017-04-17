from django.conf.urls import url

from . import views

app_name = 'constellation_base'
urlpatterns = [
    url(r'^$', views.index_view, name='Index'),
    url(r'^login$', views.login_view, name='Login'),
    url(r'^logout$', views.logout_view, name='Logout'),
    url(r'^manage/groups$', views.manage_groups.as_view(),
        name="base_manage_groups"),
    url(r'^manage/groups/delete/(?P<group_id>\d+)$',
        views.manage_group_delete,
        name="base_manage_group_delete"),
]
