import json
from urllib import parse

from faker import Faker
from requests_mock.mocker import Mocker


class BetterRequest:  # pylint: disable=too-few-public-methods
    """Better representation of PreparedRequest"""

    def __init__(self, request):
        self._request = request
        self.content_type = request.headers.get("Content-Type", "")
        self.headers = request.headers

        if self.content_type.startswith("application/x-www-form-urlencoded"):
            self.data = dict(parse.parse_qsl(request.body))
        elif self.content_type.startswith("application/json"):
            self.data = json.loads(request.body)
        else:
            self.data = request.body


class GlobalMocker(Mocker):
    """
    Global mocker class
    """

    id: str = ""
    url_prefix: str = ""
    _faker = Faker()

    def __init__(self, *args, **kwargs):
        kwargs["real_http"] = True
        super().__init__(*args, **kwargs)

    def __enter__(self):
        self.start()
        self.build_mocks()
        return self

    def build_mocks(self):
        for method in dir(self):
            if not method.startswith("mock_"):
                continue

            getattr(self, method)()

    def register_uri(self, method, url, *args, **kwargs):  # pylint: disable=arguments-differ
        if not url.startswith("http"):
            url = self.url_prefix + url
        return super().register_uri(method, url, *args, **kwargs)

    def _get_request(self, request):
        return BetterRequest(request)
