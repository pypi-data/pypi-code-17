from django.conf.urls import url
from . import views
from .Claudia import views as cv
from .Xav import views as xv
from log.views import test

urlpatterns = [
    # index page
    url(r'^$', views.index, name="index"),
    # login page
    url(r'^login/$', views.login_auth_2, name='login_page'),
    # log out view
    url(r'^logout/$', views.jump_ship, name='jump_ship'),
    # create project
    url(r'^leader_user/(?P<username>[A-Z0-9][0-9]{7})/create/$', views.create_project, name="create_project"),
    # add task
    url(r'^leader_user/(?P<username>[A-Z0-9][0-9]{7})/add/$', views.create_task, name="add_task"),
    # edit task
    url(r'^leader_user/(?P<username>[A-Z0-9][0-9]{7})/edit/(?P<pk>[0-9]{1,3})/$',
        views.TaskUpdate.as_view(username=''),
        name="leader_update_task"),
    # create member
    url(r'^leader_user/(?P<username>[A-Z0-9][0-9]{7})/add-member/$',
        views.CreateMember.as_view(username=''),
        name="create_member"),

    # members update themselves
    # url(r'^member_user/(?P<username>[A-Z0-9][0-9]{7})/update-member/$', views.update_member, name="update_member"),
    url(r"^member_user/(?P<username>[A-Z0-9][0-9]{7})/update/$", views.update_member, name='update_member'),

    # user delete view
    #url(r'^user/(?P<username>[A-Z0-9][0-9]{7})/delete/(?P<d>[A-Z0-9][0-9]{7})/$', views.delete_admin,
    #    name="delete_admin"),
    # list of users
    url(r'^user/(?P<username>[A-Z0-9][0-9]{7})/list$', views.list_users, name="list_users"),

    # task pages (now dummy pages)
    # the following will show list of open projects for the admin
    url(r'^admin_user/(?P<username>[A-Z0-9][0-9]{7})/$', views.logged_in, name="admin_home"),
    # show, create and edit tasks for specific project
    url(r'^leader_user/(?P<username>[A-Z0-9][0-9]{7})/$', views.leader_home, name="leader_home"),
    # Show member details.
    url(r'^member_user/(?P<username>[A-Z0-9][0-9]{7})/$', views.MemberHome.as_view(username=''), name="member_home"),

    # Show tasks assigned to specific user and able to upload deliverable.
    url(r'^member_user/(?P<username>[A-Z0-9][0-9]{7})/tasks$', views.show_tasks, name="task_list"),
    # user dispatch
    url(r'^user/(?P<username>[A-Z0-9][0-9]{7})/$', views.logged_in, name="user_logged_in"),

    # upload deliverable
    url(r'^member_user/(?P<username>[A-Z0-9][0-9]{7})/tasks/(?P<task>[A-Za-z0-9&\s]+)/$', views.member_upload,
        name='member_upload'),

    # ----- Claudia
    url(r"^admin_user/(?P<username>[A-Z0-9][0-9]{7})/add_admin/$", cv.create_admin_user, name='add_admin'),
    url(r"^admin_user/(?P<username>[A-Z0-9][0-9]{7})/details/$", cv.get_admin_detail, name='display_admin'),
    url(r"^admin_user/(?P<username>[A-Z0-9][0-9]{7})/update/$", cv.update_admin_detail, name='update_admin'),
    url(r"^admin_user/(?P<username>[A-Z0-9][0-9]{7})/search/$", cv.search_users, name='users_search'),
    url(r"^admin_user/(?P<username>[A-Z0-9][0-9]{7})/list/$", cv.get_list_of_users, name='list_of_users'),
    url(r"^admin_user/(?P<username>[A-Z0-9][0-9]{7})/update_user/(?P<user>[A-Z0-9][0-9]{7})/$", cv.user_update,
        name='update_user'),
    url(r"^admin_user/(?P<username>[A-Z0-9][0-9]{7})/user_detail/(?P<user>[A-Z0-9][0-9]{7})/$", cv.get_user_detail,
        name='user_detail'),
    url(r"^admin_user/(?P<username>[A-Z0-9][0-9]{7})/delete/(?P<d>[A-Z0-9][0-9]{7})/$", views.delete_user,
        name='delete_user'),
    url(r"^admin_user/(?P<username>[A-Z0-9][0-9]{7})/project/$", cv.display_all_projects, name='all_project'),
    url(r"^admin_user/(?P<username>[A-Z0-9][0-9]{7})/open_project/$", cv.display_open_projects, name='open_project'),
    url(r"^admin_user/(?P<username>[A-Z0-9][0-9]{7})/(?P<p>[a-zA-Z0-9\s]*)/project_detail/$",
        views.project_information, name='project_detail'),
    url(r"^member_user/(?P<username>[A-Z0-9][0-9]{7})/details/$", cv.get_member_detail, name='display_member'),
    url(r"^admin_user/(?P<username>[A-Z0-9][0-9]{7})/delete_project/(?P<d>[a-zA-Z0-9\s]*)/$", cv.delete_project,
        name='delete_project'),

    # ----- Xav
    # Creating a leader falls under the admin's role.
    url(r"^admin_user/(?P<username>[A-Z0-9][0-9]{7})/add_leader/$", xv.create_leader_user, name='add_leader'),
    url(r"^leader_user/(?P<username>[A-Z0-9][0-9]{7})/details/$", xv.display_leader_detail, name='display_leader'),
    url(r"^leader_user/(?P<username>[A-Z0-9][0-9]{7})/update/$", xv.update_leader_detail, name='update_leader'),
    # ----- Other
    url(r'^user/list/$', views.get_list_of_users, name='list_of_users'),

    # Log Update

    url(r'^leader_user/(?P<username>[A-Z0-9][0-9]{7})/(?P<project>[A-Za-z0-9\s]*)/log/$', test, name='leader_log'),
    url(r'^admin_user/(?P<username>[A-Z0-9][0-9]{7})/(?P<project>[A-Za-z0-9\s]*)/log/$', test, name='admin_log'),

    url(r'^leader_user/(?P<username>[A-Z0-9][0-9]{7})/list/$', views.get_list_of_members, name='members_list'),

    url(r'^leader_user/(?P<username>[A-Z0-9][0-9]{7})/delete/(?P<d>[A-Z0-9][0-9]{7})/$', views.delete_a_member,
        name='delete_member'),

    url(r'^admin_user/(?P<username>[A-Z0-9][0-9]{7})/(?P<p>[a-zA-Z0-9\s]*)/project_detail/(?P<task_pk>[0-9]+)$',
        views.send_file, name='download_deliverable')

]
