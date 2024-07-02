from django.http import HttpResponseRedirect
from django.urls import reverse


class UnexpectedRedirectPath(Exception):
    pass


class RedirectInterceptor:
    """Redirect Interceptor class"""

    id: str = ""
    url_prefix: str = ""
    url_paths: dict = {}

    def intercept(self, request, response):
        if not response.url.startswith(self.url_prefix):
            return response

        for in_path, out_name in self.url_paths.items():
            if not response.url.endswith(in_path):
                continue

            return HttpResponseRedirect(
                self.get_redirect_url(
                    request,
                    response,
                    response.url.replace(self.url_prefix, request.build_absolute_uri("/")[:-1]).replace(
                        in_path, reverse(out_name)
                    ),
                )
            )

        raise UnexpectedRedirectPath(response.url)

    def get_redirect_url(self, request, response, url):
        return url
