from django.test import TestCase, Client
from django.urls import reverse


class TestCategoryViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_category_view_redirect_user_response(self):
        url = reverse("admin-v1-category:list")
        response = self.client.get(url)
        assert response.status_code == 302
