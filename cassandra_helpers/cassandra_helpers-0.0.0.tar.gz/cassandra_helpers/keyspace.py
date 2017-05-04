from cassandra.cluster import Session


def create_keyspace(name: str,
                    *,
                    session: Session,
                    replication_class: str = 'SimpleStrategy',
                    replication_factor: int = 3,
                    check_first: bool = False) -> None:
    query = 'CREATE KEYSPACE '
    if check_first:
        query += f'IF NOT EXISTS {name} '
    else:
        query += f'{name} '
    query += (f'WITH REPLICATION = {{ \'class\' : \'{replication_class}\', '
              f'\'replication_factor\' : {replication_factor} }}')
    session.execute(query)


def drop_keyspace(name: str,
                  *,
                  session: Session) -> None:
    query = f'DROP KEYSPACE {name}'
    session.execute(query)


def keyspace_exists(name: str,
                    *,
                    session: Session) -> bool:
    query = ('SELECT (boolean)TRUE as keyspace_exists '
             'FROM system_schema.keyspaces '
             'WHERE keyspace_name = %s')
    resp = session.execute(query, parameters=(name,))
    return bool(list(resp))
