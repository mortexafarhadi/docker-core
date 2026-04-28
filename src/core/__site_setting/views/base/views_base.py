from __site_setting.views.base.views_site import get_site_setting_main
from __user._modules.register_user.views.base.views import (
    get_register_users_all,
)


def site_setting_context(context=None):
    if context is None:
        context = {}
    context["current_setting"] = get_site_setting_main()
    context["register_users_count"] = get_register_users_all().count()
    return context
