from django.apps import AppConfig
from django.conf import settings
from django.apps import apps

from cryptoassets.core.configure import Configurator
from cryptoassets.core.app import CryptoAssetsApp


class CryptoassetsConfig(AppConfig):
    name = 'cryptoassets.django'
    verbose_name = "Cryptoassets library integration for Django"

    def ready(self):
        config = getattr(settings, "CRYPTOASSETS", None)
        if not config:
            raise RuntimeError("You need to have CRYPTOASSETS configuration dictionary in your Django settings.py")

        self.cryptoassets = CryptoAssetsApp()
        self.configurator = Configurator(self.cryptoassets)
        self.configurator.load_from_dict(config)

        self.cryptoassets.setup_session()


def get_cryptoassets():
    """Return instance of cryptoassets.app.CrytoassetApp.

    """
    # Django WTF??? seriously
    app_config = apps.get_app_config('django')
    return app_config.cryptoassets
