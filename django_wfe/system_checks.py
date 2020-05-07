from django.conf import settings
from django.core import checks

from .tasks import test_dramatiq


REQUIRED_SETTINGS = [
    "WFE_WORKFLOWS",
]

IMPORTANT_OPTIONAL_SETTINGS = []


# DJANGO-WFE CHECK MESSAGES:


class MissingSettingsError(checks.Error):
    def __init__(self, setting_name, *args, **kwargs):
        super().__init__(
            f'django-wfe settings error: "{setting_name}" not found in django.conf.settings',
            hint=f'Please add "{setting_name}" to your settings.py file',
            obj=settings,
            id="django_wfe.config.E001",
            *args,
            **kwargs,
        )


class DramatiqProblemWarning(checks.Warning):
    def __init__(self, dramatiq_exception, *args, **kwargs):
        super().__init__(
            f"Sending a task to dramatiq finished with {type(dramatiq_exception).__name__}: {dramatiq_exception}",
            hint=f"Please check dramatiq and the broker are set up and are working correctly",
            obj=settings,
            id="django_wfe.dramatiq.W001",
            *args,
            **kwargs,
        )


class MissingSettingsInfo(checks.Info):
    def __init__(self, setting_name, *args, **kwargs):
        super().__init__(
            f'django-wfe settings info: "{setting_name}" was not defined, a default value will be used.',
            obj=settings,
            id="django_wfe.config.I001",
            *args,
            **kwargs,
        )


# DJANGO-WFE SYSTEM CHECKS:


@checks.register()
def settings_check(app_configs, **kwargs):
    errors = []

    for setting_name in REQUIRED_SETTINGS:
        try:
            getattr(settings, setting_name)
        except AttributeError:
            errors.append(MissingSettingsError(setting_name))

    for setting_name in IMPORTANT_OPTIONAL_SETTINGS:
        try:
            getattr(settings, setting_name)
        except AttributeError:
            errors.append(MissingSettingsInfo(setting_name))

    return errors


@checks.register()
def dramatiq_check(app_configs, **kwargs):
    errors = []

    try:
        test_dramatiq.send()
    except Exception as e:
        errors.append(DramatiqProblemWarning(e))

    return errors
