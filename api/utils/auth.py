import functools
import secrets

from flask import request, make_response

from api.models.settings import settings


def requires_auth(func):
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        auth_key = request.headers.get("Authorization")
        if not auth_key or not secrets.compare_digest(settings.API_KEY, auth_key):
            return make_response({"detail": "Not authorized"}, 401)
        return func(*args, **kwargs)
    return decorated
