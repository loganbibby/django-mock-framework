import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import path, reverse


def mock_request_view(request):
    r = requests.get("https://example.com/test")  # pylint: disable=missing-timeout
    return JsonResponse(r.json())


def redirect_view(request):
    return redirect("https://example.com/redirect")


def redirect_replace_view(request):
    return HttpResponse("hello world!")


def fake_redirect_view(request):
    return redirect("https://example.com/not_intercepted")


def normal_redirect_view(request):
    return redirect(reverse("json_view"))


def json_view(request):
    return JsonResponse({"bar": "foo"})


urlpatterns = [
    path("mock/", mock_request_view, name="mock_test_view"),
    path("redirect/", redirect_view, name="redirect_view"),
    path("redirect_replace/", redirect_replace_view, name="redirect_replace_view"),
    path("fake_redirect/", fake_redirect_view, name="fake_redirect_view"),
    path("normal_redirect/", normal_redirect_view, name="normal_redirect_view"),
    path("json/", json_view, name="json_view"),
]
