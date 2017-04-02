from __future__ import absolute_import, division, print_function, unicode_literals

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

from django.utils.functional import SimpleLazyObject

from django_otp import DEVICE_ID_SESSION_KEY, _user_is_authenticated
from django_otp.models import Device


class OTPMiddleware(MiddlewareMixin):
    """
    This must be installed after
    :class:`~django.contrib.auth.middleware.AuthenticationMiddleware` and
    performs an analagous function. Just as AuthenticationMiddleware populates
    ``request.user`` based on session data, OTPMiddleware populates
    ``request.user.otp_device`` to the :class:`~django_otp.models.Device`
    object that has verified the user, or ``None`` if the user has not been
    verified.  As a convenience, this also installs ``user.is_verified()``,
    which returns ``True`` if ``user.otp_device`` is not ``None``.
    """
    def process_request(self, request):
        user = getattr(request, 'user', None)
        if user is not None:
            request.user = SimpleLazyObject(lambda: self._verify_user(request, user))

        return None

    def _verify_user(self, request, user):
        """
        Sets OTP-related fields on an authenticated user.
        """
        user.otp_device = None
        user.is_verified = lambda: user.otp_device is not None

        if _user_is_authenticated(user):
            device_id = request.session.get(DEVICE_ID_SESSION_KEY)
            device = Device.from_persistent_id(device_id) if device_id else None

            if (device is not None) and (device.user_id != user.id):
                device = None

            if (device is None) and (DEVICE_ID_SESSION_KEY in request.session):
                del request.session[DEVICE_ID_SESSION_KEY]

            user.otp_device = device

        return user
