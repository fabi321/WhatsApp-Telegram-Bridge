import unittest
from os import remove, listdir

from BTrees.OOBTree import OOBTree

from Handlers.GeneralStorageManager import GeneralStorageManager
from Handlers.TgBotHandler import TgBotHandler
from Utilities.Pipes import Pipes
from tests.database import DatabaseObjectCreator


class HandlerTest(unittest.TestCase, DatabaseObjectCreator):
    def setUp(self) -> None:
        self.pipe: Pipes = Pipes('master')
        self.storage: GeneralStorageManager = GeneralStorageManager()
        self.storage.root.wa_users = OOBTree()
        self.wa_user_id, _, _, _, self.wa_user_storage = self.get_wa_user_storage()
        self.storage.root.wa_users[self.wa_user_id] = self.wa_user_storage
        self.storage.root.tg_users = OOBTree()
        self.tg_user_id, _, self.tg_user_storage = self.get_tg_user_storage()
        self.storage.root.tg_users[self.tg_user_id] = self.tg_user_storage
        self.storage.root.wa_groups = OOBTree()
        _, _, self.wa_group_id, self.wa_group_storage = self.get_wa_group_storage()
        self.storage.root.wa_groups[self.wa_group_id] = self.wa_group_storage
        self.storage.root.tg_groups = OOBTree()
        _, _, self.tg_group_id, self.tg_group_storage = self.get_tg_group_storage()
        self.storage.root.tg_groups[self.tg_group_id] = self.tg_group_storage
        self.storage.root.bots = OOBTree()
        self.storage.root.bots[self.wa_user_storage.tg_bot.id] = self.wa_user_storage.tg_bot
        self.storage.commit()

    def test_tg_bot_handler_creation(self):
        tg_bot_handler: TgBotHandler = TgBotHandler(bot_id=self.wa_user_storage.tg_bot.id)
        self.assertEqual(tg_bot_handler.bot_settings, self.wa_user_storage.tg_bot)
        with self.assertRaises(KeyError, msg='Accepted invalid pipe command or didn\'t create pipe'):
            self.pipe.send(str(self.wa_user_storage.tg_bot.id), 'Invalid')
            tg_bot_handler.run(once=True)

    def tearDown(self) -> None:
        self.storage.close()
        for i in listdir():
            if 'test.db' in i:
                remove(i)


if __name__ == '__main__':
    unittest.main()
