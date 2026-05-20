from decouple import config
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from _0_utils.functions.string_function import random_string, print_debug
from _0_utils.service.email_service import send_mail
from _0_utils.views.auth_view import check_user_authenticated
from _0_utils.views.base_view import render
from _1_site_setting.views.base.views_base import site_setting_context
from _2_account._modules.register_user.views.base.views import (
    get_register_user_with_email,
    get_register_user_model,
    get_register_user_with_activation_code,
)
from _2_account.views.base.views_user import (
    get_user_with_email,
    get_user_objects,
    get_user_with_reset_password_link,
)
from _2_auth.forms.forms import (
    RegisterForm,
    AccountActivationForm,
    LoginForm,
    ForgetPassForm,
    ResetPasswordForm,
)
from _2_locales import errors_en

RegisterUser = get_register_user_model()
_USE_ALLAUTH_SERVICE = settings.USE_ALLAUTH_SERVICE


class RegisterView(View):
    def get(self, request):
        _redirect = check_user_authenticated(request)
        if _redirect is not None:
            return _redirect
        else:
            register_form = RegisterForm()
            context = {"form": register_form}
            context = site_setting_context(context)
            if _USE_ALLAUTH_SERVICE:
                return render(request, "_2_auth/v1/register_with_allauth.html", context)
            else:
                return render(request, "_2_auth/v1/register.html", context)

    def post(self, request):
        _redirect = check_user_authenticated(request)
        if _redirect is not None:
            return _redirect
        else:
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                email = register_form.cleaned_data.get("email")
                first_name = register_form.cleaned_data.get("first_name")
                last_name = register_form.cleaned_data.get("last_name")
                user = get_user_with_email(email)
                if user is not None:
                    register_form.add_error(
                        "email",
                        errors_en.this_email_has_already_been_registered,
                    )
                else:
                    password = register_form.cleaned_data.get("password")
                    _pass_password_validate = False
                    try:
                        validate_password(password)
                        _pass_password_validate = True
                    except ValidationError as e:
                        register_form.add_error("password", e)
                    if _pass_password_validate:
                        send_count = 0
                        new_user = get_register_user_with_email(email)
                        if new_user is not None:
                            if new_user.diff_hours() > 0:
                                new_user.delete()
                            else:
                                if new_user.send_count > 5:
                                    context = site_setting_context()
                                    return render(
                                        request,
                                        "_2_auth/v1/error-bans.html",
                                        context,
                                    )
                                else:
                                    send_count = new_user.send_count + 1
                                    new_user.delete()

                        new_user = RegisterUser(
                            email=email,
                            first_name=first_name,
                            last_name=last_name,
                            send_count=send_count,
                        )
                        new_user.set_password(password)
                        new_user.set_activation_code()
                        context = {
                            "user": new_user,
                            "code": new_user.get_code_token(),
                        }
                        status, msg, error = send_mail(
                            "Register",
                            email,
                            context,
                            "emails/active_account.html",
                        )
                        if status:
                            new_user.save()
                            form = AccountActivationForm()
                            context = {"email": email, "form": form}
                            context = site_setting_context(context)
                            return render(
                                request,
                                "_2_auth/v1/account-activation.html",
                                context,
                            )
                        else:
                            register_form.add_error("email", f"{msg}:{error}")

            context = {"form": register_form}
            context = site_setting_context(context)
            if _USE_ALLAUTH_SERVICE:
                return render(request, "_2_auth/v1/register_with_allauth.html", context)
            else:
                return render(request, "_2_auth/v1/register.html", context)


class LoginView(View):
    def get(self, request):
        _redirect = check_user_authenticated(request)
        if _redirect is not None:
            return _redirect
        else:
            login_form = LoginForm()
            context = {"form": login_form}
            context = site_setting_context(context)
            if _USE_ALLAUTH_SERVICE:
                return render(request, "_2_auth/v1/login_with_allauth.html", context)
            else:
                return render(request, "_2_auth/v1/login.html", context)

    def post(self, request):
        _redirect = check_user_authenticated(request)
        if _redirect is not None:
            return _redirect
        else:
            login_form = LoginForm(request.POST)
            if not login_form.is_valid():
                login_form.add_error("email", errors_en.enter_the_information_correctly)
            else:
                user_email = login_form.cleaned_data.get("email")
                user_pass = login_form.cleaned_data.get("password")
                remember_me = login_form.cleaned_data.get("remember_me")
                user = get_user_with_email(user_email)
                if user is None:
                    login_form.add_error(
                        "email", errors_en.the_email_or_password_is_incorrect
                    )
                else:
                    if not user.is_active:
                        login_form.add_error(
                            "email", errors_en.your_account_is_not_active
                        )
                    else:
                        if not user.check_password(user_pass):
                            login_form.add_error(
                                "email",
                                errors_en.the_email_or_password_is_incorrect,
                            )
                        else:
                            if remember_me:
                                request.session.set_expiry(
                                    settings.REMEMBER_ME_DURATION
                                )

                            login(
                                request,
                                user,
                                backend="django.contrib.auth.backends.ModelBackend",
                            )
                            return redirect(reverse("auth-v1:dashboard"))

            context = {"form": login_form}
            if _USE_ALLAUTH_SERVICE:
                return render(request, "_2_auth/v1/login_with_allauth.html", context)
            else:
                return render(request, "_2_auth/v1/login.html", context)


@method_decorator(login_required, name="dispatch")
class DashboardView(View):

    def get_version(self):
        try:
            req_path = self.request.path
            v_index = req_path.find("/v")
            if v_index != -1:
                return req_path[v_index + 1 : v_index + 3]
        except Exception as e:
            print_debug(e)
        return "v1"

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_staff:
                if self.get_version() == "v1":
                    return redirect(reverse("admin-v1-dashboard"))
                else:
                    return redirect(reverse("admin-v2-dashboard"))
            else:
                if config("USE_PANEL_USER", default=True, cast=bool):
                    if self.get_version() == "v1":
                        return redirect(reverse("user-v1:dashboard"))
                    else:
                        return redirect(reverse("user-v2:dashboard"))
        return redirect(reverse("main:index"))


@method_decorator(login_required, name="dispatch")
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("auth-v1:login")


class AccountActivationView(View):
    def post(self, request):
        _redirect = check_user_authenticated(request)
        if _redirect is not None:
            return _redirect
        else:
            form = AccountActivationForm(request.POST)
            if form.is_valid():
                activation_code = form.cleaned_data.get("activation_code")
                user = get_register_user_with_activation_code(activation_code)
                if user is None:
                    form.add_error("activation_code", "Activation Code is Not Valid")
                else:
                    _User = get_user_objects()
                    _User.create(
                        email=user.email,
                        first_name=user.first_name,
                        last_name=user.last_name,
                        phone_number=user.phone_number,
                        password=user.password,
                        is_active=True,
                    )
                    user.delete()
                    context = site_setting_context()
                    return render(
                        request,
                        "_2_auth/v1/error-congratulations.html",
                        context,
                    )
            context = {"form": form}
            context = site_setting_context(context)
            return render(request, "_auth/v1/account-activation.html", context)


class ForgetPasswordView(View):
    def get(self, request):
        _redirect = check_user_authenticated(request)
        if _redirect is not None:
            return _redirect
        else:
            forget_pass_form = ForgetPassForm()
            context = {"form": forget_pass_form}
            context = site_setting_context(context)
            return render(request, "_auth/v1/forget-password.html", context)

    def post(self, request):
        _redirect = check_user_authenticated(request)
        if _redirect is not None:
            return _redirect
        else:
            forget_pass_form = ForgetPassForm(request.POST)
            errors = []
            if not forget_pass_form.is_valid():
                errors.append(errors_en.enter_the_information_correctly)
            else:
                user_email = forget_pass_form.cleaned_data.get("email")
                user = get_user_with_email(user_email)
                if user is None:
                    errors.append(errors_en.mail_send_to_email)
                else:
                    user.reset_password_link = random_string(250)
                    context = {"user": user, "code": user.reset_password_link}
                    status, msg, error = send_mail(
                        "Recovery Password",
                        user.email,
                        context,
                        "emails/forget_password.html",
                    )
                    if status:
                        user.save()
                    else:
                        errors.append(f"{msg}:{error}")

            context = {"errors": errors}
            context = site_setting_context(context)
            return render(
                request,
                "_auth/v1/error-send-mail-reset-password.html",
                context,
            )


class ResetPasswordView(View):
    def get(self, request, reset_pass_link):
        _redirect = check_user_authenticated(request)
        if _redirect is not None:
            return _redirect
        else:
            user = get_user_with_reset_password_link(reset_pass_link)
            if user is None:
                return redirect(reverse("auth-v1:login"))
            else:
                reset_pass_form = ResetPasswordForm()
                context = {"form": reset_pass_form}
                context = site_setting_context(context)
                return render(request, "_auth/v1/reset-password.html", context)

    def post(self, request, reset_pass_link):
        _redirect = check_user_authenticated(request)
        if _redirect is not None:
            return _redirect
        else:
            reset_pass_form = ResetPasswordForm(request.POST)
            if reset_pass_form.is_valid():
                user = get_user_with_reset_password_link(reset_pass_link)
                if user is None:
                    return redirect(reverse("auth-v1:login"))
                else:
                    new_pass = reset_pass_form.cleaned_data.get("password")
                    try:
                        validate_password(new_pass)
                        user.set_password(new_pass)
                        user.reset_password_link = random_string(250)
                        user.save()
                        return redirect(reverse("auth-v1:login"))
                    except ValidationError as e:
                        reset_pass_form.add_error("password", e)

            context = {"form": reset_pass_form}
            return render(request, "_auth/v1/reset-password.html", context)


def __resend_code(request):
    if request.method == "POST":
        email = request.POST.get("email")
        form = AccountActivationForm()
        if email is not None:
            user = get_register_user_with_email(email)
            if user is not None:
                if user.send_count > 5:
                    context = site_setting_context()
                    return render(request, "_auth/v1/error-bans.html", context)
                else:
                    context = {"user": user, "code": user.get_code_token()}
                    status, msg, error = send_mail(
                        "Activation Code",
                        user.email,
                        context,
                        "emails/active_account.html",
                    )
                    if status:
                        user.send_count += 1
                        user.save()
                        context = {"email": email, "form": form}
                        return render(
                            request,
                            "_auth/v1/account-activation.html",
                            context,
                        )

    return redirect(reverse("auth-v1:login"))
