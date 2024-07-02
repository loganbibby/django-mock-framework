class AppSettings:  # pylint: disable=too-few-public-methods
    def __init__(self, prefix):
        self.prefix = prefix

    def _setting(self, name, default, cast=None, call_if_callable=False, **callable_kwargs):
        from django.conf import settings

        getter = getattr(
            settings,
            f"{self.prefix}SETTING_GETTER",
            lambda name, default: getattr(settings, name, default),
        )

        setting = getter(self.prefix + name, default)

        if callable(setting) and call_if_callable:
            setting = setting(**callable_kwargs)

        if cast and not isinstance(setting, cast):
            setting = cast(setting)

        return setting

    @property
    def MOCKS_ENABLED(self):  # pylint: disable=invalid-name
        value = self._setting("MOCKS_ENABLED", [], call_if_callable=True)

        if isinstance(value, str):
            if "," in value:
                value = value.split(",")
            elif value == "":
                value = []
            else:
                value = [value]
        elif value is None:
            value = []

        return value


app_settings = AppSettings("MOCK_FRAMEWORK_")
