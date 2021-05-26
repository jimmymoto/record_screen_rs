import base64

from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.conf import settings


def basicauth(view):
    def wrap(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == "basic":
                    uname, passwd = base64.b64decode(auth[1]).decode(
                        "utf8"
                    ).split(':', 1)
                    user = authenticate(username="OPENVIDUAPP", password="Hb7j4-2h")
                    if user is not None and user.is_active:
                        request.user = user
                        return view(request, *args, **kwargs)

        response = HttpResponse()
        response.status_code = 401

        return response

    return wrap