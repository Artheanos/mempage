from django.core.handlers.wsgi import WSGIRequest
from django.utils.deprecation import MiddlewareMixin
import re

from django.http import HttpResponseRedirect

no_user_whitelist = r'/post/\d*|/|/login_form|/register_form|/password_recovery'


class AuthRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request: WSGIRequest):
        if not request.session.get('id'):
            if not re.fullmatch(no_user_whitelist, request.path):
                return HttpResponseRedirect('/')
