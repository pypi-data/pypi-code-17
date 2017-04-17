from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout
from django.conf import settings
from django.utils.module_loading import import_module
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.views import View
from django.db import transaction

from .forms import LoginForm
from .models import GlobalTemplateSettings
from .models import LocalGroupACLEntry

@login_required
def index_view(request):
    template_settings_object = GlobalTemplateSettings(allowBackground=True)
    template_settings = template_settings_object.settings_dict()
    constellation_apps = []
    for appname in settings.INSTALLED_APPS:
        if "django" not in appname:
            app = import_module(appname)
            if hasattr(app, 'views') and hasattr(app.views, 'view_dashboard'):
                constellation_apps.append({
                    'name': appname,
                    'url': reverse(appname + ':' + 'view_dashboard')
                })

    return render(request, 'constellation_base/index.html', {
        'template_settings': template_settings,
        'apps': constellation_apps,
    })


def login_view(request):
    template_settings_object = GlobalTemplateSettings(allowBackground=True)
    template_settings = template_settings_object.settings_dict()
    form = LoginForm(request.POST or None)
    if "next" in request.GET:
        next_page = request.GET["next"]
    else:
        next_page = "/"
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            if request.POST["next"]:
                return HttpResponseRedirect(request.POST["next"])
            else:
                return HttpResponseRedirect("/")
    return render(request, 'constellation_base/login.html', {
        'form': form,
        'template_settings': template_settings,
        'next': next_page,
    })


def logout_view(request):
    logout(request)
    return redirect("constellation_base:Login")


@method_decorator(staff_member_required, name='dispatch')
class manage_groups(View):

    def get(self, request):
        """Show a list of the supplemental groups"""
        template_settings_object = GlobalTemplateSettings(allowBackground=True)
        template_settings = template_settings_object.settings_dict()

        existing_groups = LocalGroupACLEntry.objects.values_list('group',
                                                                 flat=True)
        existing_groups = Group.objects.filter(pk__in=set(existing_groups))

        all_groups = Group.objects.all()

        return render(request, 'constellation_base/group_list.html', {
            'template_settings': template_settings,
            'existing_groups': existing_groups,
            'all_groups': all_groups
        })

    def post(self, request):

        with transaction.atomic():
            group = Group.objects.get(name=request.POST["group_id"])
            # Clear the old membership entries

            LocalGroupACLEntry.objects.filter(group=group).delete()

            members = request.POST["membership_listing"]
            members = members.split(",")
            for member in members:
                lgacle = LocalGroupACLEntry()
                lgacle.username = member
                lgacle.group = group
                lgacle.save()

        return redirect('constellation_base:base_manage_groups')


@staff_member_required
def manage_group_delete(request, group_id):
    """Delete a group ACL"""
    with transaction.atomic():
        group = Group.objects.get(pk=group_id)
        LocalGroupACLEntry.objects.filter(group=group).delete()

    return redirect('constellation_base:base_manage_groups')
