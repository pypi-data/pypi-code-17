class MySQLHelper:

    def __init__(self, connect_params):
        self.__params = connect_params

    def __call__(self, *args, **kwargs):
        return self.mysqlexecute(*args, **kwargs)

    async def mysqlexecute(self, sql, CursorClass):
        import aiomysql
        from aiomysql.cursors import Cursor

        if not issubclass(CursorClass, Cursor):
            raise TypeError(f"""cursor class must be subclass of
                aiomysql.cursor.Cursor, given {CursorClass.__name__}""")

        if not sql:
            return ()

        async with aiomysql.connect(**self.__params) as connection:
            async with connection.cursor(CursorClass) as cursor:
                await cursor.execute(sql)
                return await cursor.fetchall()


class DbHelper:
    from .configuration import config
    from motor.motor_asyncio import AsyncIOMotorClient

    mysql = MySQLHelper(dict(
        host=config['worker']['mysql']['host'],
        port=config['worker']['mysql']['port'],
        user=config['worker']['mysql']['user'],
        password=config['worker']['mysql']['password'],
        db=config['worker']['mysql']['asteriskdb']
    ))

    mongo = AsyncIOMotorClient(
        config['worker']['mongo']['url'],
        connectTimeoutMS=config['worker']['mongo']['connect_timeout_ms'],
        serverSelectionTimeoutMS=config['worker']['mongo']['server_selection_timeout_ms']
    )
