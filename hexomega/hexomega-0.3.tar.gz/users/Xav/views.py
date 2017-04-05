from users.views import *

from .add_leader_form import *

from django.db.utils import IntegrityError


def create_leader_user(request, username):
    form = LeaderForm()
    if request.method == 'POST':
        form = LeaderForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = get_default_password()
            try:
                user = LeaderUser.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                      email=email, password=password)
            except IntegrityError as e:
                return render(request, 'users/leaderuser_form.html',
                              {'form': form, 'mail_error': 'The email is not unique!'})

            user.set_password(password)
            mail_kickoff(user, password)
            user.save()
            update_session_auth_hash(request, request.user)
            return redirect('display_admin', request.user.username)
    return render(request, 'users/leaderuser_form.html', {'form': form})


@login_required
def display_leader_detail(request, username):
    user = LeaderUser.objects.get(username__iexact=username)
    return render(request, 'users/leaderdetail.html', {'user': user})


@login_required
def update_leader_detail(request, username):
    user = LeaderUser.objects.get(username__iexact=username)
    form_data = {'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name,
                 'email': user.email,
                 'password': user.password, 'bio': user.bio}
    form = UpdateLeaderForm(request.POST, initial=form_data)
    if request.method == 'POST':
        print(form.errors)
        if form.is_valid():
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            pw = request.POST['password']
            if (pw is not '' or pw is not None) and len(pw.strip()) >= 8:
                user.set_password(pw)
            user.bio = request.POST.get('bio')
            user.save()
            messages.add_message(request, messages.WARNING, 'User Profile has been altered.\n'
                                                            'Please login again.')
            logout(request)
            update_session_auth_hash(request, request.user)
            return redirect('display_leader', username)

    return render(request, 'users/update_leader_form.html', {'user': user, 'form': form, 'errors': form.errors})
