from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MockFrameworkConfig(AppConfig):
    name = "mock_framework"
    verbose_name = _("Mock Framework")
    verbose_name_plural = _("Mock Framework")
