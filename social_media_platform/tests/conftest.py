import os

import django
import pytest
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.setting.tests")
django.setup()


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
