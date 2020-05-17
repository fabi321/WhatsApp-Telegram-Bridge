from ZODB.Connection import Connection
from ZODB.DB import DB
from transaction import commit

from Utilities.config import Config


class GeneralStorageManager:
    db: DB = DB(Config.SETTINGS['db_path'])

    def __init__(self):
        self._connection: Connection = self.db.open()
        self.root = self._connection.root()
        self.commit = commit

    def close(self) -> None:
        self._connection.close()
        self.db.close()
