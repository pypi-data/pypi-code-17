import mimetypes

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import Group

from HexOmega.settings import BASE_DIR
from .utils import get_default_password, mail_kickoff, uploaded_file_handler
from .models import Project, AdminUser, MemberUser, LeaderUser, Task, User
from .backends import CustomUserAuth
from .forms.login_form import LoginForm
from .forms.project_forms import CreateProjectForm
from .forms.task_forms import CreateTaskForm, LeaderUpdateTaskForm
from .forms.member_form import MemberUpdate, MemberCreate

from .Xav.user_context import url_context

from log.Log import log

import os
from datetime import datetime, timedelta


def index(request):
    return render(request,
                  'users/index.html')


def login_auth_2(request):
    """
    Login page authentication using django forms.
    If easier and simpler, implement this else the
    stuff I threw together up there.
    :param request:
    :return:
    """
    if request.user.is_authenticated():
        return redirect('user_logged_in', request.user.username)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            rem = request.POST.get('rem')
            user = CustomUserAuth().authenticate(username=username, password=password)

            if user is False:
                form.errors['password'] = 'The username or password is incorrect.'
                return render(request,
                              'users/login.html',
                              {
                                  'form': form,
                                  'errors': form.errors
                              })

            if user is not None:
                print('User [{}] is logging in.'.format(user.username))
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                if rem is not None:
                    request.session.set_expiry(7200)
                else:
                    request.session.set_expiry(1800)
                return redirect('user_logged_in', username=username)

    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


@login_required
def logged_in(request, username):
    if AdminUser.objects.filter(username__exact=username).count() == 1:
        return redirect('open_project', username)
    elif LeaderUser.objects.filter(username__exact=username).count() == 1:
        return redirect('leader_home', username)
    else:
        user = MemberUser.objects.get(username__exact=username)
        return redirect('task_list', username)


@login_required
def jump_ship(request):
    print('jumping ship....')
    logout(request)
    return redirect('login_page')


@login_required
def delete_user(request, username, d):
    if User.objects.get(username__iexact=d):
        person = User.objects.get(username__iexact=d)
        from django.db import IntegrityError
        try:
            if d != '10101010':
                person.delete()
        except IntegrityError as ie:
            from django.contrib import messages
            messages.add_message(request, messages.WARNING,
                                 'Cannot delete leader without closing and deleting a project.')
    return redirect('list_of_users', username)


@login_required
def member_upload(request, username, task):
    t = Task.objects.get(title=task)
    done = None
    if 'up_file' in request.FILES:
        if t.est_end.date() > datetime.now().date():
            t.deliverable = request.FILES['up_file']
            t.save()
            mail_kickoff(MemberUser.objects.get(username__exact=username), t, var=3)
            log('SUCCESS', MemberUser.objects.get(username__exact=username),
                '{} uploaded a deliverable for {}'.format(username, t.title))
            print(t.deliverable.url)
            return redirect('task_list', username)
        else:
            done = True
            return render(request, 'list.html', {
                'username': username,
                'done': True
            })
    else:
        print('No file!!')
    return render(request, 'list.html', {
        'username': username,
        'done': done
    })


@login_required
def list_users(request, username):
    return render(request, 'list.html', {'admins': AdminUser.objects.all()})


@login_required
@url_context
def get_list_of_users(request):
    """
    Display a list of admin users
    /list/
    :param request:
    :return:
    :author Caroline
    """
    admin_user_list = AdminUser.objects.order_by('pk')
    paginator = Paginator(admin_user_list, 1)  # Show 3 admin per page

    page = request.GET.get('page')
    try:
        admin_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        admin_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        admin_list = paginator.page(paginator.num_pages)
    context = {'admin_list': admin_list, 'page': page}
    return render(request, 'users/list_of_users.html', context)


# ============================================================================
# Release Me!
@login_required
def leader_home(request, username):
    user = LeaderUser.objects.get(username__exact=username)
    try:
        tasks = user.project.actionlist.task_set.all()
        for task in Task.objects.filter(action_list__project__leader__username=username):
            print(task.title, task.action_list.project.name)
            # print(task.deliverable.url)
    except Exception as e:
        print('Ahhhhhh')
        tasks = None
    return render(request, 'leader_home.html', {'user': user, 'tasks': tasks})


class CreateMember(CreateView, LoginRequiredMixin):
    # fields = ['username', 'first_name', 'last_name', 'role', 'email', 'phone']
    form_class = MemberCreate
    username = ''
    model = MemberUser
    l = None
    template_name = 'create_member.html'

    def form_valid(self, form):
        try:
            form.instance.project = self.l.project
        except self.l.project.DoesNotExist as np:
            # from django.contrib import messages
            messages.add_message(self.request, messages.WARNING,
                                 'Cannot add members to a project without a project.\nPlease create a project first.')
        password = get_default_password()
        form.instance.set_password(password)
        mail_kickoff(form.instance, password)
        messages.add_message(self.request, messages.INFO, 'User [{}] created.'.format(form.instance.username))
        update_session_auth_hash(self.request, self.request.user)
        return super(CreateMember, self).form_valid(form)

    def get_form_kwargs(self):
        self.l = LeaderUser.objects.get(username__exact=self.request.user.username)
        p = self.request.get_full_path()
        print(p)
        self.success_url = '/'.join(p.split('/')[:-1]) + '/'
        kwargs = super(CreateMember, self).get_form_kwargs()
        # kwargs['pn'] = l.project.name
        return kwargs


class MemberHome(DetailView, LoginRequiredMixin):
    model = MemberUser
    username = ''
    template_name = 'member_home.html'

    def get_object(self, queryset=None):
        return MemberUser.objects.get(username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        context = super(MemberHome, self).get_context_data(**kwargs)
        return context


@login_required
def show_tasks(request, username):
    ts = Task.objects.filter(members__username=username)
    print(ts)
    return render(request, 'list.html', {'tasks': ts})


# ============================================================================
# My project and tasks modules
# 2017-03-22

def get_project_path(p):
    return os.path.join(BASE_DIR,
                        os.path.join('projects', p.name + '/'))


@login_required
def create_project(request, username):
    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            p.leader = LeaderUser.objects.get(username__exact=username)
            p.save()
            for a in request.POST.get('admins'):
                p.admins.add(a)
            path = get_project_path(p)
            # os.makedirs(path, 0o755)
            if not os.path.exists(path):
                os.makedirs(path, 0o755)
            if not os.path.exists(os.path.join(path, 'activity.log')):
                f = open(os.path.join(path, 'activity.log'), 'w+')
                f.close()
        return redirect('display_leader', username)
    else:
        form = CreateProjectForm()

    return render(request, 'crproj.html', {'form': form})


@login_required
def create_task(request, username):
    l = LeaderUser.objects.get(username__exact=username)
    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            mem_dat = form.cleaned_data.get('members')
            title = form.cleaned_data.get('title')
            est_end = form.cleaned_data.get('est_end')
            status = form.cleaned_data.get('status')
            lt = form.cleaned_data.get('to_leader')
            if lt is None:
                lt = False
            t = Task.objects.create(title=title, est_end=est_end, status=status, to_leader=lt,
                                    action_list=l.project.actionlist)
            t.save()

            for m in mem_dat:
                t.members.add(m)
            t.save()
            log('INFO', l, '{} added a new Task [{}]'.format(l.username, t.title))
            return redirect('leader_home', username)
        else:
            print(form.errors)
    else:
        form = CreateTaskForm({'pn': l.project.name})

    return render(request, 'crtask.html', {'form': form})


class TaskUpdate(UpdateView, LoginRequiredMixin):
    username = ''
    model = Task
    template_name = 'crtask.html'
    content_type = 'multipart-form-data'
    form_class = LeaderUpdateTaskForm

    def get_form_kwargs(self):
        l = LeaderUser.objects.get(username__exact=self.request.user.username)
        t = Task.objects.get(pk=self.kwargs['pk'])
        up_flag = False
        up_name = ''
        if bool(t.deliverable):
            up_flag = True
            up_name = t.deliverable.name.split('/')[-1]
            t.status = 'Completed'
            t.save()
            log('SUCCESS', l, '{} uploaded a deliverable to Task [{}]'.format(l.username, t.title))
            mail_kickoff(l, t, var=3)
        p = self.request.get_full_path()
        self.success_url = '/'.join(p.split('/')[:-3]) + '/'
        kwargs = super(TaskUpdate, self).get_form_kwargs()
        kwargs['pn'] = l.project.name
        kwargs['up_flag'] = up_flag
        kwargs['up_name'] = up_name
        log('INFO', l, '{} made changes to Task [{}]'.format(l.username, t.title))
        return kwargs


@login_required
def update_member(request, username):
    mem = MemberUser.objects.get(username__exact=username)
    form = MemberUpdate(request.POST, initial={
        'first_name': mem.first_name,
        'last_name': mem.last_name,
        'email': mem.email,
        'phone': mem.phone
    })
    if request.method == 'POST':
        if form.is_valid():
            fn = request.POST.get('first_name')
            ln = request.POST.get('last_name')
            email = request.POST.get('email')
            p = request.POST.get('password')
            ph = request.POST.get('phone')
            if fn is not '':
                mem.first_name = fn
            if ln is not '':
                mem.last_name = ln
            if email is not '':
                mem.email = email
            if (p is not None and p is not '') and len(p.strip()) >= 8:
                mem.set_password(p)
            if ph is not '':
                mem.phone = ph
            if mem.has_usable_password():
                update_session_auth_hash(request, mem)
                mem.save()
                logout(request)
                from django.contrib import messages
                messages.add_message(request, messages.INFO, 'Your profile was altered. Please login again.')
                return redirect('login_page')
        else:
            print(form.errors)
    else:
        form = MemberUpdate()

    return render(request, 'update_member.html', {
        'form': form,
        'user': mem,
        'title': 'Update'
    })


def get_list_of_members(request, username):
    member_user_list = MemberUser.objects.order_by('pk').filter(project__leader__username=username)
    user = LeaderUser.objects.get(username__iexact=username)
    paginator = Paginator(member_user_list, 10)  # Show 3 admin per page

    page = request.GET.get('page')
    try:
        member_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        member_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        member_list = paginator.page(paginator.num_pages)
    context = {'member_list': member_list, 'page': page, 'user': user}
    return render(request, 'users/list_of_members.html', context)


def delete_a_member(request, username, d):
    if MemberUser.objects.get(username__iexact=d):
        person = MemberUser.objects.get(username__iexact=d)
        person.delete()
    return redirect('members_list', username)


@login_required
def project_information(request, username, p):
    print('Yoohoo!')
    project = Project.objects.get(name__exact=p)
    for p in project.actionlist.task_set.all():
        print(p.deliverable.name.split('/')[-1])
    return render(request, 'users/project_information.html', {'project': project})


@login_required
def send_file(request, username, p, task_pk):
    task = Task.objects.get(pk=int(task_pk))
    file_path = '/' + task.deliverable.url
    print(task)
    if '%20' in file_path:
        file_path = file_path.replace('%20', ' ')
    file_mimetype = mimetypes.guess_type(file_path)
    # if os.path.exists(file_path):
    try:
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type=file_mimetype)
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    # else:
    except Exception as e:
        return HttpResponse('File retrieval error. <br>' + file_path + '<br>' + str(e))
