from .models import User, AdminUser, LeaderUser, MemberUser


class CustomUserAuth(object):
    def authenticate(self, username=None, password=None):
        try:
            user = None
            if AdminUser.objects.filter(username__exact=username).count() == 1:
                # print('ADMIN')
                user = AdminUser.objects.get(username__exact=username)
            elif LeaderUser.objects.filter(username__exact=username).count() == 1:
                # print('LEADER')
                user = LeaderUser.objects.get(username__exact=username)
            elif MemberUser.objects.filter(username__exact=username).count() == 1:
                # print('MEMBER')
                user = MemberUser.objects.get(username__exact=username)
            elif User.objects.filter(username__exact=username).count() == 1:
                # print('USER')
                user = User.objects.get(username__exact=username)

            if user is not None and user.check_password(password):
                return user
            else:
                return False

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = None
            if AdminUser.objects.filter(pk=user_id).count() == 1:
                user = AdminUser.objects.get(pk=user_id)
            elif LeaderUser.objects.filter(pk=user_id).count() == 1:
                user = LeaderUser.objects.get(pk=user_id)
            elif MemberUser.objects.filter(pk=user_id).count() == 1:
                user = MemberUser.objects.get(pk=user_id)
            elif User.objects.filter(pk=user_id).count() == 1:
                user = User.objects.get(pk=user_id)

            if user.is_active:
                return user

        except User.DoesNotExist:
            return None
