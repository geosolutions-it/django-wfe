from django.conf import settings

# Python path to the user defined Workflows, e.g.: 'django_wfe_integration.workflows'
WORKFLOWS = getattr(settings, "WFE_WORKFLOWS", None)


# Interval between updates of the WDK models in seconds
WATCHDOG_INTERVAL = getattr(settings, "WFE_WATCHDOG_INTERVAL", 5)
