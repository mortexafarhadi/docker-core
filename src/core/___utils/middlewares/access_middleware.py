from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse


class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if path.find("/panel-admin/") > 0:
            if not request.user.is_authenticated:
                return redirect(reverse("auth-v1:login"))
            if not request.user.is_staff:
                return HttpResponseForbidden(
                    "You do not have permission to access this section."
                )

        response = self.get_response(request)
        return response
