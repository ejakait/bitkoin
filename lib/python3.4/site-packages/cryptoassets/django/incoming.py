"""Notify Django about incoming tx updates."""

from django import db

from .signals import txupdate


def handle_tx_update(event_name, data):
    """Post a transaction status update."""
    txupdate.send(handle_tx_update, event_name=event_name, data=data)

    # Make Django to close its own database connection,
    # so that each new event doesn't consume leave connection open
    db.close_connection()
