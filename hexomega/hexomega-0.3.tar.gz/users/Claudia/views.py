from django.db import IntegrityError

from users.views import *

from .user_form import AdminUserForm, AdminUpdateForm, UserUpdateForm

from users.models import User

from users.filters import SearchFilter


@login_required
def create_admin_user(request, username):
    """
    Create an admin user.
    username/add/$
    :param username:
    :param request:
    :return:
    """
    form = AdminUserForm()
    if request.method == 'POST':
        form = AdminUserForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = get_default_password()
            # bio = request.POST.get('bio')
            user = AdminUser.objects.create(username=username, first_name=first_name, last_name=last_name,
                                            email=email)
            user.set_password(password)
            mail_kickoff(user, password)
            user.save()
            update_session_auth_hash(request, request.user)
            return redirect('display_admin', request.user.username)
    return render(request, 'users/adminuser_form.html', {'form': form})


@login_required
def get_admin_detail(request, username):
    """
    Display the information of an admin user
    :param request:
    :return:
    """
    user = AdminUser.objects.get(username__iexact=username)
    return render(request, 'users/user_information.html', {'adminuser': user})


@login_required
def get_member_detail(request, username):
    """
    Display the information of a member user
    :param request:
    :param username:
    :return:
    """
    user = MemberUser.objects.get(username__iexact=username)
    return render(request, 'users/member_information.html', {'memberuser': user})


# abhi's test decorator : removed from repo
# @viewing_context
@login_required
def update_admin_detail(request, username):
    """
    Update the information of an admin user from "edit profile"
    :param request:
    :param username:
    :return:
    """
    user = AdminUser.objects.get(username__iexact=username)
    form_data = {'first_name': user.first_name, 'last_name': user.last_name,
                 'email': user.email, 'password': " ", 'bio': user.bio}
    form = AdminUpdateForm(request.POST, initial=form_data)
    if request.method == 'POST':
        print(form.errors)
        if form.is_valid():
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            p = request.POST['password']
            if (p is not '' or p is not None) and len(p.strip()) >= 8:
                user.set_password(p)
            user.bio = request.POST.get('bio')
            user.save()
            update_session_auth_hash(request, request.user)
            return redirect('display_admin', username)

    return render(request, 'users/update_admin_form.html', {'adminuser': user, 'form': form, 'errors': form.errors})


@login_required
def display_all_projects(request, username):
    """
    Display all projects
    :param request:
    :param username:
    :return:
    """
    project_list = Project.objects.all().order_by('pk')
    proj_paginator = Paginator(project_list, 10)
    proj_page = request.GET.get('page')

    try:
        all_project_list = proj_paginator.page(proj_page)
    except PageNotAnInteger:
        all_project_list = proj_paginator.page(1)
    except EmptyPage:
        all_project_list = proj_paginator.page(proj_paginator.num_pages)

    return render(request, 'users/all_project_list.html', {'all_project_list': all_project_list, 'page': proj_page})


@login_required
def display_open_projects(request, username):
    """
    Display a list of open projects
    :param request:
    :param username:
    :return:
    """
    open_proj_list = Project.objects.filter(status='0').order_by('pk')
    open_proj_paginator = Paginator(open_proj_list, 10)
    open_proj_page = request.GET.get('page')

    try:
        open_project_list = open_proj_paginator.page(open_proj_page)
    except PageNotAnInteger:
        open_project_list = open_proj_paginator.page(1)
    except EmptyPage:
        open_project_list = open_proj_paginator.page(open_proj_paginator.num_pages)
    return render(request, 'users/open_project_list.html',
                  {'open_project_list': open_project_list, 'page': open_proj_page})


@login_required
def project_information(request, username, p):
    """
    Display a particular project information
    :param request:
    :param username:
    :param p:
    :return:
    """
    project = Project.objects.get(name__exact=p)
    for p in project.actionlist.task_set.all():
        print(p.deliverable.name.split('/')[-1])
    return render(request, 'users/project_information.html', {'project': project})


@login_required
def user_update(request, username, user):
    """
    Update a user particulars (email and password)
    :param request:
    :param username:
    :param user:
    :return:
    """
    adm = AdminUser.objects.get(username=username)
    person = User.objects.get(username__iexact=user)
    form_data = {'email': person.email, 'password': " "}
    form = UserUpdateForm(request.POST, initial=form_data)
    if request.method == 'POST':
        if form.is_valid() and user != '10101010':
            person.email = request.POST.get('email')
            pw = request.POST['password']
            if (pw is not '' or pw is not None) and len(pw.strip()) >= 8:
                person.set_password(pw)
            person.save()
            update_session_auth_hash(request, request.user)
            return redirect('list_of_users', username)
    return render(request, 'users/user_update_form.html', {'form': form, 'errors': form.errors, 'user': person})


@login_required
def get_list_of_users(request, username):
    """
    Display a list of all users (admins, leaders and members)
    :param request:
    :param username:
    :return:
    """
    person = User.objects.get(username__iexact=username)
    list_of_users = User.objects.exclude(username__iexact='AnonymousUser')
    paginator = Paginator(list_of_users, 10)
    page = request.GET.get('page')
    try:
        all_users_list = paginator.page(page)
    except PageNotAnInteger:
        all_users_list = paginator.page(1)
    except EmptyPage:
        all_users_list = paginator.page(paginator.num_pages)

    context = {'user': person, 'all_users_list': all_users_list, 'page': page}
    return render(request, 'users/list_of_users.html', context)


@login_required
def get_user_detail(request, username, user):
    """
    Display the user detail from the list of all users
    :param request:
    :param username:
    :param user:
    :return:
    """
    person = User.objects.get(username__iexact=user)
    return render(request, 'users/user_information.html', {'user': person})


@login_required
def search_users(request, username):
    """
    Search for all users
    :param request:
    :param username:
    :return:
    """
    if 'username' in request.GET or 'first_name' in request.GET or 'last_name' in request.GET:
        queryset = User.objects.exclude(username__iexact='AnonymousUser')
        result_list = SearchFilter(request.GET, queryset=queryset)
        return render(request, 'users/search.html', {'result_list': result_list})
    return render(request, 'users/search.html')


def delete_project(request, username, d):
    """
    Delete a project from the system
    :param request:
    :param username:
    :param d:
    :return:
    """
    if Project.objects.get(name__iexact=d):
        project = Project.objects.get(name__iexact=d)
        try:
            project.delete()
        except IntegrityError as ie:
            messages.add_message(request, messages.WARNING,
                                 'A project consists of members.\n'
                                 'Please delete all members prior to deleting a project.')
    return redirect('all_project', username)
