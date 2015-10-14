from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.conf import settings

from cryptoassets.core.service.main import Service


class Command(BaseCommand):

    help = "Create database tables for cryptoassets based on the current cryptocurrency configuration"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """ """
        config = settings.CRYPTOASSETS
        service = Service(config)
        service.initialize_db()
