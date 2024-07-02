from contextlib import ExitStack

from class_registry.registry import RegistryKeyError
from django.http import HttpResponseRedirect

from .app_settings import app_settings
from .registries import mocker_registry, redirect_interceptor_registry


class MockMiddlewareBase:  # pylint: disable=too-few-public-methods
    """Base middleware for mocks"""

    def __init__(self, get_response):
        self.get_response = get_response

    def get_enabled_mocks(self):
        return app_settings.MOCKS_ENABLED


class MockerMiddleware(MockMiddlewareBase):
    """Middleware to wrap responses with mocks"""

    def __call__(self, request):
        with ExitStack() as exit_stack:
            for mock_id in self.get_enabled_mocks():
                try:
                    exit_stack.enter_context(mocker_registry[mock_id])
                except RegistryKeyError:
                    continue

            return self.get_response(request)


class RedirectInterceptorMiddleware(MockMiddlewareBase):
    """Middleware to intercept redirects for mocks"""

    def __call__(self, request):
        response = self.get_response(request)

        if not isinstance(response, HttpResponseRedirect):
            return response

        for mock_id in self.get_enabled_mocks():
            try:
                response = redirect_interceptor_registry[mock_id].intercept(request, response)
            except RegistryKeyError:
                continue

        return response
