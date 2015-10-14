"""
"""
from cryptoassets.django.app import get_cryptoassets


def managed_transaction(func):
    """Handle the decorated function inside ConflictResolver managed transaction.

    http://cryptoassetscore.readthedocs.org/en/latest/api/utils.html#module-cryptoassets.core.utils.conflictresolver
    """
    app = get_cryptoassets()
    return app.conflict_resolver.managed_transaction(func)
