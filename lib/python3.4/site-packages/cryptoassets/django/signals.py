"""Django signals integration."""

import django.dispatch

txupdate = django.dispatch.Signal(providing_args=["event_name", "data"])
