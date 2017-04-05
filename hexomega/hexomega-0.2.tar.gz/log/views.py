from django.shortcuts import render, HttpResponse

from users.models import Project, AdminUser, LeaderUser

from .parse_to_html import parse_log
from yattag import Doc


# Create your views here.
def test(request, username, project):
    user = ''
    if AdminUser.objects.filter(username__exact=username).count() is 1:
        user = AdminUser.objects.get(username__exact=username)
    else:
        user = LeaderUser.objects.get(username__exact=username)

    if Project.objects.filter(name__exact=project).exists():
        proj = Project.objects.get(name__exact=project)
    elif Project.objects.filter(leader__username=username):
        proj = user.project
    else:
        print(username)
        print('------->>' + project + '<<---------')
        return HttpResponse("No project created yet. Please create a project first.")

    doc, tag, text = Doc().tagtext()
    with tag('h3', id='main-title'):
        text(project)

    p = parse_log(proj)
    return render(request, 'log/test.html',
                  {'log_data': p.test(),
                   'project_title': doc.getvalue(),
                   'title': proj.name,
                   'section': 'Log',
                   'user': user
                   })
