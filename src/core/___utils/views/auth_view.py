from django.shortcuts import redirect
from django.urls import reverse


def check_user_authenticated(request):
    user = request.user
    if user.is_authenticated:
        return redirect(reverse("auth-v1:dashboard"))
    else:
        return None
