from django.core.management.base import BaseCommand
from django.conf import settings

from cryptoassets.core.service.main import Service
from cryptoassets.core.app import ALL_SUBSYSTEMS


class Command(BaseCommand):

    help = "Run cryptoassets helper service within Django project"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """ """
        config = settings.CRYPTOASSETS
        # We do not need to initialize logging as Django does it for us
        service = Service(config, ALL_SUBSYSTEMS, logging=False)
        service.start()
