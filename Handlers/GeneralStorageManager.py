from ZODB.DB import DB

from Utilities.config import Config


class GeneralStorageManager:
    __db: DB = DB(Config.SETTINGS['db_path'])
    _connection = __db.open()
