from django.urls import path

from ...views import views as vv

app_name = "auth-v2"

urlpatterns = [
    path("register/", vv.RegisterView.as_view(), name="register"),
    path("login/", vv.LoginView.as_view(), name="login"),
    path("dashboard/", vv.DashboardView.as_view(), name="dashboard"),
    path("logout/", vv.LogoutView.as_view(), name="logout"),
    path("forget-pass/", vv.ForgetPasswordView.as_view(), name="forget-pass"),
    path(
        "reset-pass/<reset_pass_link>/",
        vv.ResetPasswordView.as_view(),
        name="reset-pass",
    ),
    path(
        "account-activation/",
        vv.AccountActivationView.as_view(),
        name="account-activation",
    ),
    path("resend-code-register/", vv.__resend_code, name="resend-code-register"),
]
