import base64
import binascii
from api.utils import jwt_decode
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _

from api.models import User


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get("HTTP_AUTHORIZATION", b"")
    if isinstance(auth, str):
        auth = auth.split(" ")
    return auth


class CustomJwtAuthentication:
    keyword = "octoxlabs"

    def authenticate(self, request):
        """
        Returns a `User` if a correct username and password have been supplied
        using JWT authentication.  Otherwise returns `None`.
        """
        auth = get_authorization_header(request)

        if not auth or auth[0].lower() != self.keyword:
            raise exceptions.AuthenticationFailed(_("Invalid token type."))

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed(
                _("Invalid jwt token header. No credentials provided.")
            )
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed(
                _(
                    "Invalid jwt token header. Credentials string should not contain spaces."
                )
            )

        try:
            auth_decoded = jwt_decode(auth[1])
        except Exception as e:
            raise exceptions.AuthenticationFailed(_(str(e)))

        userid = auth_decoded["user_id"]
        return self.authenticate_credentials(userid, request)

    def authenticate_credentials(self, userid, request=None):
        """
        Authenticate the userid and password against username and password
        with optional request for context.
        """
        try:
            user = User.objects.get(id=userid)
        except Exception as e:
            raise exceptions.AuthenticationFailed(_(str(e)))
        return (user, None)

    def authenticate_header(self, request):
        return self.keyword
