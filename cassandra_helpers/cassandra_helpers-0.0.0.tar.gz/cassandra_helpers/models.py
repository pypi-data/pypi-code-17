from typing import Iterable

from cassandra.connection import Connection
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model


def sync_tables(*models: Model,
                keyspaces_names: Iterable[str] = None,
                connections: Iterable[Connection] = None
                ) -> None:
    for model in models:
        sync_table(model,
                   keyspaces=keyspaces_names,
                   connections=connections)
