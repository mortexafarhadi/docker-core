import os
from io import BytesIO
from urllib.request import urlopen

from django.core.files import File
from ___utils.views.base_view import render
from faker import Faker

from __site_setting.models.models import SiteSetting


def fake_site_setting(request, count):
    if request.method == "GET":
        fake = Faker()
        url = "https://picsum.photos/1024/1024"
        if count is not None and count > 0:
            for _ in range(count):
                response_logo1 = urlopen(url)
                image_content_logo1 = BytesIO(response_logo1.read())
                filename_logo1 = os.path.basename(url)
                response_logo2 = urlopen(url)
                image_content_logo2 = BytesIO(response_logo2.read())
                filename_logo2 = os.path.basename(url)
                setting = SiteSetting(
                    site_name=fake.name(),
                    email=fake.email(),
                    phone=fake.phone_number(),
                    fax=fake.phone_number(),
                    address=fake.address(),
                    copyright=fake.text(max_nb_chars=20),
                    is_main=fake.pybool(),
                )
                setting.logo_1.save(
                    filename_logo1, File(image_content_logo1), save=True
                )
                setting.logo_2.save(
                    filename_logo2, File(image_content_logo2), save=True
                )
                setting.save()

            context = {
                "model": "Site Settings",
                "count": count,
            }
            return render(request, "__fake_data/fake-data.html", context)
