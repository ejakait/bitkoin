Cryptoassets library integration for Django
=============================================

This package provides integration of `cryptoassets.core <https://bitbucket.org/miohtama/cryptoassets>`_ Bitcoin and  cryptoasset framework for `Django web framework <http://djangoproject.com/>`_.

.. contents :: :local:

Features
=================

* Use Django ``settings.py`` configure mechanism to set up *cryptoassets.core*

* Django management command mappings for `cryptoassets helper service <http://cryptoassetscore.readthedocs.org/en/latest/service.html>`_

* Django native logging

* Django event dispatch integration

* Setting up SQLAlchemy sessions and database conflict resolution inside Django

Usage
=================

Add ``cryptoassets.django`` to your Django application list in ``settings.py``::

    INSTALLED_APPS = (
        'cryptoassets.django',
    )

Add `cryptoassets.core configuration <http://cryptoassetscore.readthedocs.org/en/latest/config.html>`_ as Python dictionary to your Django ``settings.py`` module under ``CRYPTOASSETS`` variable.

Example for ``settings.py``::

    # TESTNET settings
    CRYPTOASSETS = {

        # It is recommended to use separate database for cryptoassets,
        # but you can share the database with Django as well.
        # In any case, cryptoassets
        # will use a separate db connection.
        # cryptoassets.django does not read the existing DATABASES setting.
        # Configure the connection using SQLAlchemy syntax:
        # http://cryptoassetscore.readthedocs.org/en/latest/config.html#database
        "database": {
            "url": "postgresql://localhost/cryptoassets",
            "echo": False,
        },

        # Configure block.io API service with Bitcoin testnet
        # (let's not play around with real Bitcoins yet)
        "coins": {
            "btc": {
                "backend": {
                    "class": "cryptoassets.core.backend.blockio.BlockIo",
                    "api_key": "923f-xxxx-yyyy-zzzz",
                    "network": "btctest",
                    "pin": "foobar123",
                    # Cryptoassets helper process will use this UNIX named pipe to communicate
                    # with bitcoind
                    "walletnotify": {
                        "class": "cryptoassets.core.backend.sochainwalletnotify.SochainWalletNotifyHandler",
                        "pusher_app_key": "e9f5cc20074501ca7395"
                    },
                }
            },
        },

        # Bind cryptoassets.core event handler to Django dispacth wrapper
        "events": {
            "django": {
                "class": "cryptoassets.core.event.python.InProcessEventHandler",
                "callback": "cryptoassets.django.incoming.handle_tx_update"
            }
        },

        # Start simple status at port 9001 for diagnostics
        "status_server": {
            "ip": "127.0.0.1",
            "port": 9001
        }
    }

.. note ::

    If you copy-paste these settings please sign up at block.io for your own API key.

Initializing database
-----------------------

Run::

    python manage.py cryptoassets_initialize_database

This will build database tables for configured cryptocurrencies.

This is Django management command warpper for `cryptoassets-initialize-database <http://cryptoassetscore.readthedocs.org/en/latest/service.html#cryptoassets-initialize-database>`_.

Starting cryptoassets helper service
-------------------------------------

Start a helper service. This standalone process runs, connects to APIs and networks, listens to incoming transactions, broadcasts outgoing transaction.

.. note ::

    Cryptoassets helper service does not run within your web server process. It runs as a standalone process on your server.

Run::

    python manage.py cryptoassets_helper_service

For more information see `helper service command <http://cryptoassetscore.readthedocs.org/en/latest/service.html#cryptoassets-helper-service>`_.

Handling incoming transactions
-------------------------------

Make sure ``walletnotify`` is configured in ``CRYPTOASSETS`` setting as described above. It will translate incoming interprocess communication to Django events.

Grab incoming transactions in your application code in ``txupdate`` signal::

    from cryptoassets.django.signals import txupdate
    from django.dispatch import receiver

    @receiver(txupdate)
    def txupdate_received(event_name, data, **kwargs):
        """ Received transaction update from cryptoassets.core.

        """

        if data.get("transaction_type") != "deposit":
            # We are only interest updates on incoming transctions
            return

        transaction_hash = data["txid"]
        value = data['amount']
        address = data['address']
        confirmations = int(data.get('confirmations', -1))

        logger.info("Transaction update received: %s BTC:%s address:%s confirmations:%d", transaction_hash, value, address, confirmations)

The handler is executed inside *cryptoassets helper service* process.

`More information about cryptoassets.core events <http://cryptoassetscore.readthedocs.org/en/latest/api/events.html>`_.

Accessing cryptoassets data
=============================

Accessing database models
-------------------------
To get access to database models::

    from cryptoassets.django.app import get_cryptoassets

    cryptoassets = get_cryptoassets()
    BitcoinWallet = cryptoassets.coins.get("btc").coin_description.Wallet

Making database queries
-------------------------

All database access goes through a separate SQLAlcemy session which is wrapped with `database transaction conflict resolver <http://cryptoassetscore.readthedocs.org/en/latest/api/utils.html#module-cryptoassets.core.utils.conflictresolver>`_.

For convenience, ``cryptoassets.django.assetsdb.managed_transaction()`` decorator is provided:

Example code::

    from cryptoassets.django.app import get_cryptoassets
    from cryptoassets.django import assetdb

    def get_wallet(session):
        """Return the master shared wallet used to receive payments. """
        cryptoassets = get_cryptoassets()
        BitcoinWallet = cryptoassets.coins.get("btc").coin_description.Wallet
        wallet = BitcoinWallet.get_or_create_by_name("default", session)
        return wallet

    def create_new_receiving_address(label):

        @assetdb.managed_transaction
        def tx(session):

            wallet = get_wallet(session=session)

            account = wallet.get_or_create_account_by_name("my account")
            session.flush()  # account id gets written inside commit
            addr = wallet.create_receiving_address(account, label)
            logging.info("Created receiving address %s", addr.address)
            address = addr.address
            return address

        return tx()

The rest is by `model API <http://cryptoassetscore.readthedocs.org/en/latest/api/models.html>`_ and `SQLAlchemy <http://cryptoassetscore.readthedocs.org/en/latest/gettingstarted.html#more-about-sqlalchemy>`_.

Other
=================

Example Django application
----------------------------

`See Liberty Music Store <http://libertymusicstore.net/>`_ (`source code <https://github.com/miohtama/LibertyMusicStore>`_).

cryptoassets.core tutorial
---------------------------

`See getting started <http://cryptoassetscore.readthedocs.org/en/latest/gettingstarted.html>`_.

Running helper service as system service
----------------------------------------

To have automatic start/stop and other functionality for cryptoassets helper service, use something akin *systemd* or `supervisord <http://supervisord.org/>`_ to manage ``python manage.py cryptoassets_helper_service``.

Author
=================

Mikko Ohtamaa (`blog <https://opensourcehacker.com>`_, `Facebook <https://www.facebook.com/?q=#/pages/Open-Source-Hacker/181710458567630>`_, `Twitter <https://twitter.com/moo9000>`_, `Google+ <https://plus.google.com/u/0/103323677227728078543/>`_)

