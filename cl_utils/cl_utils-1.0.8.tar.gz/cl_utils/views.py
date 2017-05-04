import os
import random

import django
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth import views as auth_views
from django.contrib.sites.models import Site
from django.contrib.sites.requests import RequestSite
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import check_for_language
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.utils import translation

from cl_utils.forms import LoginForm
try:
    from localeurl import utils
    def change_language_in_path(path, language):
        locale,path = utils.strip_path(path)
        if locale:
            return utils.locale_path(path, language)
        else:
            return path
except:
    import re
    def change_language_in_path(path, language):
        path = re.sub('^/[a-z]{2}/', '/%s/' % (language,), path) # TODO handle things like en-us
        return path


def set_language_on_response(request, response, lang_code):
    'Set the language in session & in cookie on the response'
    if hasattr(request, 'session'):
        request.session['django_language'] = lang_code
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    translation.activate(lang_code)


def random_image(request, sub_dir=None):
    if sub_dir is None:
        img_dir = settings.MEDIA_ROOT
    else:
        img_dir = '%s%s/' % (settings.MEDIA_ROOT, sub_dir)

    img_list = []
    for root, dirs, files in os.walk(img_dir):
        for name in files:
            filename = os.path.join(root, name)
            img_list.append(os.path.join(root.replace(img_dir, ''), name))

        if '.svn' in dirs:
            dirs.remove('.svn')

    img = img_list[random.randint(0, len(img_list) - 1)]
    return HttpResponseRedirect('%s%s/%s' % (settings.MEDIA_URL, sub_dir, img))


def login(request,
          template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=LoginForm):
    '''
    Displays the login form and handles the login action.
    When the User is logged on, we'll try to read the language from his/her
    profile and update the current language accordingly.
    '''
    if django.VERSION < (1, 2):
        response = auth_views.login(request, template_name=template_name, redirect_field_name=redirect_field_name)
    else:
        response = auth_views.login(request, template_name=template_name, redirect_field_name=redirect_field_name, authentication_form=authentication_form)

    if request.method == 'POST':
        try:
            p = request.user.get_profile()
        except AttributeError:
            lang_code = translation.get_language()
        except ObjectDoesNotExist:
            lang_code = translation.get_language()
        else:
            lang_code = p.language

            if lang_code == '':
                lang_code = translation.get_language()
                p.language = lang_code
                p.save()
        set_language_on_response(request, response, lang_code)

    return response


def login_or_register(request,
                      template_name='registration/login.html',
                      redirect_field_name=REDIRECT_FIELD_NAME,
                      registration_view='',
                      authentication_form=LoginForm):
    '''
    Displays the login form and handles the login action.
    If the email is not registered, redirect to registration page
    '''
    redirect_to = get_from_request(request, redirect_field_name, '')
    if request.method == 'POST':
        form = authentication_form(data=request.POST)
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            from django.contrib.auth import login
            login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return HttpResponseRedirect(redirect_to)
        elif not getattr(form, 'found_user', True) and not registration_view == '':
            return HttpResponseRedirect(reverse(registration_view))
    else:
        form = authentication_form(request)
    request.session.set_test_cookie()
    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)
    return render_to_response(template_name, {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }, context_instance=RequestContext(request))


def set_language(request, next=None):
    '''
    Redirect to a given url while setting the chosen language in the
    session or cookie. The url and the language code need to be
    specified in the request parameters.
    Try to save the new language in the User's profile.
    '''
    next = next \
        or get_from_request(request, 'next', None) \
        or request.META.get('HTTP_REFERER', None) \
        or '/'

    response = HttpResponseRedirect(next)
    if request.method == 'GET' or request.method == 'POST':
        lang_code = get_from_request(request, 'language', settings.LANGUAGE_CODE)
        if check_for_language(lang_code):
            # update the language in the url if it's in there
            next = change_language_in_path(next, lang_code)
            response = HttpResponseRedirect(next)

            set_language_on_response(request, response, lang_code)

            # Try to save language in the user profile,
            # unless a staff user is logged in as that user (via django-token-auth)
            if request.user.is_authenticated() and not request.session.get('token_auth_impersonating', False):
                try:
                    p = request.user.get_profile()
                    p.language = lang_code
                    p.save()
                except:
                    pass

    return response


def handler500(request):
    'Simple 500 handler (only add MEDIA_URL)'
    resp = render_to_response('500.html',
                              {'MEDIA_URL': settings.MEDIA_URL},
                              context_instance=RequestContext(request))
    resp.status_code = 500
    return resp


def get_from_request(request, key, default):
    '''
    Since the REQUEST attribute (a merge of the POST/GET dicts) is removed in Django 1.9,
    this is a shorthand for getting a value from the POST/GET attributes.
    '''
    if request.method == 'POST':
        return request.POST.get(key, default)
    else:
        return request.GET.get(key, default)
