from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from ..serializers.user_serializer import UserSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from django.forms.models import model_to_dict
from django.conf import settings
from rest_framework.permissions import AllowAny

class UserRegistrationView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        #first check if username already exists
        if 'first_name' not in data:
            return JsonResponse('first name is a required field', status=200, safe=False)
        if 'last_name' not in data:
            return JsonResponse('last_name is a required field', status=200, safe=False)
        if 'username' not in data:
            return JsonResponse('username is a required field', status=200, safe=False)
        if 'password' not in data:
            return JsonResponse('password is a required field', status=200, safe=False)
        if 'email' not in data:
            return JsonResponse('email is a required field', status=200, safe=False)

        user_exists = User.objects.filter(username=data['username'])
        if user_exists:
            return JsonResponse('user already exists', status=200, safe=False)
        user_s = UserSerializer(data=data)

        #save new user
        if(user_s.is_valid()):
            user_s.save()
            saved_user = User.objects.get(pk=user_s.data['id'])
            if saved_user:
                #add user to user group
                try:
                    g = Group.objects.get(name=settings.JOLI_USERS_USER_GROUP_NAME)
                except Exception as e:
                    return JsonResponse(error='no user groups created', status=200)
                g.user_set.add(saved_user.id)

                #send user confirmation email
                token = Token.objects.filter(user_id=saved_user.id)
                if token:
                    token = token.first()
                    # try:
                    #     verify_link = request.get_host() +  '/eventstaff/users/confirm_account/?verify_id=' + token
                    #     msg = EmailMessage(
                    #         settings.JOLI_USERS_EMAIL_SUBJECT,
                    #         'Hi ' + user.first_name + ' ' + user.last_name + ', <br><br> ' + JOLI_USERS_EMAIL_BODY_TEXT + '. Please follow this link ' + verify_link,
                    #         settings.JOLI_USERS_EMAIL_FROM,
                    #         [user.email],
                    #     )
                    #     msg.content_subtype = "html"
                    #     msg.send()
                    # except Exception as e:
                    #     return JsonResponse(model_to_dict(e), status=200)

                    return JsonResponse(model_to_dict(token), status=200, safe=False)
                else:
                    return JsonResponse('No user token created', status=200, safe=False)
            else:
                return JsonResponse('error saving user', status=200, safe=False)

        return JsonResponse('attempted to save an invalid user', status=200, safe=False)
