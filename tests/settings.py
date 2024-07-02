SECRET_KEY = "fake-key"

INSTALLED_APPS = [
    "tests",
]

MIDDLEWARE = ["mock_framework.middleware.MockerMiddleware", "mock_framework.middleware.RedirectInterceptorMiddleware"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "test.db",
    }
}

ROOT_URLCONF = "tests.views"

MOCK_FRAMEWORK_MOCKS_ENABLED = ["test"]
