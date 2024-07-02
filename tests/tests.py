import requests
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from mock_framework import (
    GlobalMocker,
    RedirectInterceptor,
    UnexpectedRedirectPath,
    mocker_registry,
    redirect_interceptor_registry,
)
from mock_framework.app_settings import app_settings


@mocker_registry.register
class TestMocker(GlobalMocker):
    id = "test"
    url_prefix = "https://example.com"

    def mock_test(self):
        self.register_uri("get", "/test", json={"foo": "bar"})


@redirect_interceptor_registry.register
class TestRedirectInterceptor(RedirectInterceptor):
    id = "test"
    url_prefix = "https://example.com"
    url_paths = {"/redirect": "redirect_replace_view"}


class GlobalMockerTestCase(TestCase):
    def test_mock(self):
        with TestMocker():
            r = requests.get("https://example.com/test")  # pylint: disable=missing-timeout
            self.assertEqual(r.json(), {"foo": "bar"})

    def test_middleware(self):
        r = Client().get(reverse("mock_test_view"))

        self.assertEqual(r.json()["foo"], "bar")

    def test_real_http(self):
        with TestMocker():
            r = requests.get("https://httpbin.org/get")  # pylint: disable=missing-timeout
            self.assertEqual(r.json().get("url"), "https://httpbin.org/get")


class RedirectInterceptorTestCase(TestCase):
    def test_middleware(self):
        r = Client().get(reverse("redirect_view"), follow=True)

        self.assertEqual(r.wsgi_request.get_full_path(), reverse("redirect_replace_view"))

        self.assertEqual(r.status_code, 200)

        self.assertEqual(r.content.decode(), "hello world!")

    def test_unexpected_redirect_path(self):
        self.assertRaises(UnexpectedRedirectPath, lambda: Client().get(reverse("fake_redirect_view")))

    def test_normal_redirect(self):
        r = Client().get(reverse("normal_redirect_view"), follow=True)

        self.assertEqual(r.json(), {"bar": "foo"})


class AppSettingsTestCase(TestCase):
    @override_settings(MOCK_FRAMEWORK_MOCKS_ENABLED=["test"])
    def test_mocks_enabled_as_list(self):
        self.assertEqual(app_settings.MOCKS_ENABLED, ["test"])

    @override_settings(MOCK_FRAMEWORK_MOCKS_ENABLED="test")
    def test_mocks_enabled_as_str(self):
        self.assertEqual(app_settings.MOCKS_ENABLED, ["test"])

    @override_settings(MOCK_FRAMEWORK_MOCKS_ENABLED="test,test2")
    def test_mocks_enabled_as_csv(self):
        self.assertEqual(app_settings.MOCKS_ENABLED, ["test", "test2"])

    @override_settings(MOCK_FRAMEWORK_MOCKS_ENABLED="")
    def test_mocks_enabled_as_empty_str(self):
        self.assertEqual(app_settings.MOCKS_ENABLED, [])

    @override_settings(MOCK_FRAMEWORK_MOCKS_ENABLED=None)
    def test_mocks_enabled_as_none(self):
        self.assertEqual(app_settings.MOCKS_ENABLED, [])
