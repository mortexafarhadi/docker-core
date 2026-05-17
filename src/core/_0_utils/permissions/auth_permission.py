from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def superuser_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden(
                "You do not have permission to view this page."
            )
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden(
                "You do not have permission to view this page."
            )
        return view_func(request, *args, **kwargs)

    return _wrapped_view
