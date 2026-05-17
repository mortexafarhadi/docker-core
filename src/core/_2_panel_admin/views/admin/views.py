from _0_utils.views.base_view import TemplateView


class DashboardView(TemplateView):
    def get_version(self):
        try:
            req_path = self.request.path
            v_index = req_path.find("/v")
            if v_index != -1:
                return req_path[v_index + 1 : v_index + 3]
        except Exception as e:
            print(e)
        return "v1"

    def get_template_names(self):
        if self.request.user.is_authenticated:
            if self.get_version() == "v1":
                return "_2_panel_admin/v1/dashboard.html"
            else:
                return "_2_panel_admin/v2/dashboard.html"
            # if self.request.user.is_superuser:
            # return '_2_panel_admin/v1/dashboard.html'
        else:
            return "_2_panel_admin/v1/dashboard.html"
