import unittest
from ZODB import DB
import os
from DBModels.ConversationStorage import ConversationStorage
from DBModels.MessageStorage import MessageStorage
from DBModels.UserStorage import UserStorage
from DBModels.TgUserStorage import TgUserStorage
from DBModels.WaUserStorage import WaUserStorage
from DBModels.TgBotStorage import TgBotStorage
from DBModels.GroupStorage import GroupStorage
from DBModels.TgGroupStorage import TgGroupStorage
from DBModels.WaGroupStorage import WaGroupStorage
from DBModels.UserConversationStorage import UserConversationStorage
from DBModels.GroupConversationStorage import GroupConversationStorage
from Attachments.GenericAttachment import GenericAttachment
from Utilities.typings import *
from typing import Dict, Tuple


class DatabaseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.db = DB(None)
        self.conn = self.db.open()
        self.root = self.conn.root()
        with open('picture.jpg', 'w') as f:
            f.write('Hello World')

    @classmethod
    def get_user_storage(self) -> Tuple[AccountName, UserStorage]:
        user_name: AccountName = AccountName('name')
        user_storage: UserStorage = UserStorage(user_name)
        return user_name, user_storage

    def get_tg_user_storage(self) -> Tuple[TgUserId, AccountName, TgUserStorage]:
        user_name, _ = self.get_user_storage()
        user_id: TgUserId = TgUserId('id')
        user_storage: TgUserStorage = TgUserStorage(id=user_id, name=user_name)
        return user_id, user_name, user_storage

    def get_wa_user_storage(self) -> Tuple[WaNumber, AccountName, TgBotId, TgBotToken, WaUserStorage]:
        user_name, _ = self.get_user_storage()
        user_id: WaNumber = WaNumber(123)
        bot_id: TgBotId = TgBotId(123)
        bot_token: TgBotToken = TgBotToken('abc')
        user_storage: WaUserStorage = WaUserStorage(id=user_id, name=user_name, tg_bot_id=bot_id,
                                                    tg_bot_token=bot_token)
        return user_id, user_name, bot_id, bot_token, user_storage

    def get_tg_message_variables(self) -> Tuple[TgUserStorage, MessageText, TgMessageId, GenericAttachment]:
        user_id, user_name, user_storage = self.get_tg_user_storage()
        message_text: MessageText = MessageText('text')
        id: TgMessageId = TgMessageId(123456)
        attachment: GenericAttachment = GenericAttachment()
        return user_storage, message_text, id, attachment

    def get_wa_message_variables(self) -> Tuple[WaUserStorage, WaMessageId, MessageText]:
        user_id, user_name, bot_id, bot_token, user_storage = self.get_wa_user_storage()
        id: WaMessageId = WaMessageId(123456)
        message_text: MessageText = MessageText('text')
        return user_storage, id, message_text

    def get_tg_message_storage(self) -> Tuple[TgUserStorage, MessageText, TgMessageId, MessageStorage,
                                              GenericAttachment]:
        user_storage, message_text, id, attachment = self.get_tg_message_variables()
        message_storage = MessageStorage(sender=user_storage, text=message_text, tg_id=id, attachment=attachment)
        return user_storage, message_text, id, message_storage, attachment

    def get_wa_message_storage(self) -> Tuple[WaUserStorage, MessageText, WaMessageId, MessageStorage]:
        user_storage, id, message_text = self.get_wa_message_variables()
        message_storage: MessageStorage = MessageStorage(text=message_text, sender=user_storage, wa_id=id)
        return user_storage, message_text, id, message_storage

    @classmethod
    def get_group_storage(self) -> Tuple[GroupName, GroupDescription, GroupStorage]:
        group_name: GroupName = GroupName('abc')
        group_description: GroupDescription = GroupDescription('def')
        group_storage: GroupStorage = GroupStorage(name=group_name, description=group_description)
        return group_name, group_description, group_storage

    def test_user_storage_creation(self):
        user_name, user_storage = self.get_user_storage()
        self.assertEqual(user_storage.name, user_name, msg='got different name than given')
        self.assertEqual(user_storage.get_type_name(), 'User', msg='UserStorage is not named User')
        self.assertFalse(user_storage.picture, msg='picture is true, but not given')
        self.assertIsNone(user_storage.picture_path, msg='picture_path is set, but not given')
        with self.assertRaises(AttributeError, msg='got auth_id without self.id'):
            user_storage.auth_id()
        with self.assertRaises(AttributeError, msg='got str(user_storage) without self.id'):
            str(user_storage)
        with self.assertRaises(AssertionError, msg='accepted string as name'):
            UserStorage(name='name')

    def test_user_storage_picture(self):
        user_name, user_storage = self.get_user_storage()
        picture_path: FilePath = FilePath('picture.jpg')
        with self.assertRaises(FileNotFoundError, msg='returned picture_path, but no picture given'):
            user_storage.get_picture()
        with self.assertRaises(FileNotFoundError, msg='accepted picture without picture_path'):
            UserStorage(name=user_name, picture=True)
        with self.assertRaises(FileNotFoundError, msg='accepted nonexistent picture_path'):
            UserStorage(name=user_name, picture=True, picture_path='nonexistent')
        with self.assertRaises(AssertionError, msg='accepted string as picture_path'):
            UserStorage(name=user_name, picture=True, picture_path='picture.jpg')
        user_storage.add_picture(picture_path=picture_path)
        self.assertTrue(user_storage.picture, msg='picture is false, but picture was set afterwards')
        self.assertEqual(user_storage.get_picture(), picture_path, msg='got different picture_path than set afterwards')
        user_storage: UserStorage = UserStorage(name=user_name, picture=True, picture_path=picture_path)
        self.assertTrue(user_storage.picture, msg='picture is false, but picture was given')
        self.assertEqual(user_storage.get_picture(), picture_path, msg='got different picture_path than given')

    def test_user_storage_auth_id(self):
        class Subclass(UserStorage):
            def __init__(self, id):
                name: AccountName = AccountName('name')
                super().__init__(name=name)
                self.id = id
        test_strings: Dict[str, str] = {'123': '123', '-123': 'm123', '12-3': '12m3'}
        for i, j in test_strings.items():
            user_storage: Subclass = Subclass(i)
            self.assertEqual(user_storage.auth_id(), j, msg='wrong auth_string generation')
            self.assertEqual(str(user_storage), i, msg='wrong string result')
            self.assertIsInstance(str(user_storage), str, msg="str() method doesn't return str")

    def test_tg_user_storage_creation(self):
        user_id, user_name, user_storage = self.get_tg_user_storage()
        self.assertEqual(user_storage.id, user_id, msg='got different id than given')
        self.assertEqual(user_storage.get_type_name(), 'TgUser', msg='TgUserStorage is not named TgUser')
        with self.assertRaises(AssertionError, msg='accepted string as id'):
            TgUserStorage(id='id', name=user_name)

    def test_wa_user_storage_creation(self):
        user_id, user_name, bot_id, bot_token, user_storage = self.get_wa_user_storage()
        self.assertEqual(user_storage.id, user_id, msg='got different id than given')
        self.assertEqual(user_storage.get_type_name(), 'WaUser', msg='WaUserStorage is not named WaUser')
        self.assertEqual(user_storage, user_storage.tg_bot.wa_user,
                         msg='WaUserStorage of TgBotStorage is not equal to original WaUserStorage')
        self.assertIs(user_storage, user_storage.tg_bot.wa_user,
                      msg='WaUserStorage of TgBotStorage is not exactly the same as  original WaUserStorage')
        with self.assertRaises(AssertionError, msg='accepted integer as id'):
            WaUserStorage(id=123, name=user_name, tg_bot_id=bot_id, tg_bot_token=bot_token)

    def test_tg_bot_storage_creation(self):
        user_id, user_name, bot_id, bot_token, user_storage = self.get_wa_user_storage()
        user_storage: TgBotStorage = user_storage.tg_bot
        self.assertEqual(user_storage.id, bot_id, msg='got different id than given')
        self.assertEqual(user_storage.token, bot_token, msg='got different token than given')
        self.assertEqual(user_storage.get_type_name(), 'TgBot', msg='TgBotStorage is not named TgBot')
        with self.assertRaises(AssertionError, msg='accepted integer as id'):
            WaUserStorage(id=user_id, name=user_name, tg_bot_id=123, tg_bot_token=bot_token)
        with self.assertRaises(AssertionError, msg='accepted string as token'):
            WaUserStorage(id=user_id, name=user_name, tg_bot_id=bot_id, tg_bot_token='abc')
        with self.assertRaises(AssertionError, msg='accepted invalid wa_user'):
            TgBotStorage(id=bot_id, token=bot_token, wa_user='123')

    def test_message_storage_creation_equals(self):
        tg_user_storage, tg_message_text, tg_id, tg_message_storage, attachment = self.get_tg_message_storage()
        wa_user_storage, wa_message_text, wa_id, wa_message_storage = self.get_wa_message_storage()
        reply_message: MessageStorage = MessageStorage(text=tg_message_text, sender=tg_user_storage, tg_id=tg_id,
                                                       reply_to=tg_message_storage)
        self.assertIs(tg_message_storage.sender, tg_user_storage, msg='got different tg_sender than given')
        self.assertEqual(tg_message_storage.text, tg_message_text, msg='got different text than given')
        self.assertEqual(tg_message_storage.tg_id, tg_id, msg='got different tg_id than given')
        self.assertEqual(wa_message_storage.wa_id, wa_id, msg='got different wa_id than given')
        self.assertIs(tg_message_storage.attachment, attachment, msg='got different attachment than given')
        self.assertIsNone(tg_message_storage.reply_to, msg='got reply_message but none was given')
        self.assertIs(reply_message.reply_to, tg_message_storage, msg='got different reply_message than given')
        self.assertIsNone(reply_message.wa_id, msg='got wa_id, but none was given')
        self.assertIsNone(reply_message.attachment, msg='got attachment, but none was given')
        self.assertFalse(tg_message_storage.download, msg='download set to true but not downloaded yet')
        self.assertFalse(tg_message_storage.delivered, msg='delivered set to true but nothing delivered yet')
        self.assertIs(wa_message_storage.sender, wa_user_storage, msg='got different wa_sender than given')
        self.assertTrue(wa_message_storage.download, msg='download st to false, but nothing to download')

    def test_message_storage_creation_fails(self):
        tg_user_storage, tg_message_text, tg_id, tg_message_storage, attachment = self.get_tg_message_storage()
        wa_user_storage, wa_message_text, wa_id, wa_message_storage = self.get_wa_message_storage()
        with self.assertRaises(AssertionError, msg='accepted string as text'):
            MessageStorage(text='text', sender=wa_user_storage, wa_id=wa_id)
        with self.assertRaises(AssertionError, msg='accepted wa_sender with only tg_id'):
            MessageStorage(text=tg_message_text, sender=wa_user_storage, tg_id=tg_id)
        with self.assertRaises(AssertionError, msg='accepted tg_sender with only wa_id'):
            MessageStorage(text=tg_message_text, sender=tg_user_storage, wa_id=wa_id)
        with self.assertRaises(AttributeError, msg='accepted no message_id'):
            MessageStorage(text=tg_message_text, sender=wa_user_storage)
        with self.assertRaises(AssertionError, msg='accepted int as tg_id'):
            MessageStorage(text=tg_message_text, sender=tg_user_storage, tg_id=123456)
        with self.assertRaises(AssertionError, msg='accepted int as wa_id'):
            MessageStorage(text=tg_message_text, sender=wa_user_storage, wa_id=123456)
        with self.assertRaises(AssertionError, msg='accepted invalid attachment'):
            MessageStorage(text=tg_message_text, sender=tg_user_storage, tg_id=tg_id, attachment='123')
        with self.assertRaises(AssertionError, msg='accepted invalid reply_to'):
            MessageStorage(text=tg_message_text, sender=tg_user_storage, tg_id=tg_id, reply_to='123')

    def test_conversation_storage_creation(self):
        _, _, _, message_storage, _ = self.get_tg_message_storage()
        conversation_storage: ConversationStorage = ConversationStorage()
        self.assertEqual(conversation_storage.messages, [], msg='got messages but none given')
        conversation_storage: ConversationStorage = ConversationStorage(messages=[message_storage])
        self.assertEqual(conversation_storage.messages, [message_storage], msg='got different messages than given')
        self.assertIs(conversation_storage.messages[0], message_storage,
                      msg='got message that is not exactly the same as given')
        with self.assertRaises(AssertionError, msg='accepted invalid message'):
            ConversationStorage(messages=['abc'])

    def test_conversation_storage_message_handling(self):
        _, _, tg_id, tg_message_storage, _ = self.get_tg_message_storage()
        _, _, wa_id, wa_message_storage = self.get_wa_message_storage()
        conversation_storage: ConversationStorage = ConversationStorage()
        conversation_storage.add_message(message=tg_message_storage)
        self.assertEqual(conversation_storage.messages, [tg_message_storage], msg='got different messages than given')
        self.assertIs(conversation_storage.messages[0], tg_message_storage,
                      msg='got message that is not exactly the same as given')
        conversation_storage.add_message(message=tg_message_storage)
        self.assertEqual(conversation_storage.messages, [tg_message_storage], msg='added already existing')
        with self.assertRaises(AssertionError, msg='add_message accepted invalid message'):
            conversation_storage.add_message('')
        conversation_storage.remove_message(message=tg_message_storage)
        self.assertEqual(conversation_storage.messages, [], 'got messages left after removing the only one')
        with self.assertRaises(AttributeError, msg='removed nonexistent message'):
            conversation_storage.remove_message(message=tg_message_storage)
        conversation_storage.add_message(message=tg_message_storage)
        conversation_storage.remove_message_by_id(message_id=tg_id)
        self.assertEqual(conversation_storage.messages, [], 'got messages left after removing by tg_id')
        conversation_storage.add_message(wa_message_storage)
        conversation_storage.remove_message_by_id(message_id=wa_id)
        self.assertEqual(conversation_storage.messages, [], msg='got messages left after removing by wa_id')
        with self.assertRaises(AssertionError, msg='remove_by_id accepted invalid id'):
            conversation_storage.remove_message_by_id(123)

    def test_group_storage_creation(self):
        group_name, group_description, group_storage = self.get_group_storage()
        user_name, user_storage = self.get_user_storage()
        self.assertEqual(group_storage.name, group_name, msg='got different name than expected')
        self.assertEqual(group_storage.description, group_description, msg='got different description than expected')
        group_storage: GroupStorage = GroupStorage(name=group_name, description=group_description, users=[user_storage])
        self.assertEqual(group_storage.users, [user_storage], msg='got different users than given')
        self.assertIs(group_storage.users[0], user_storage, msg='got user that is not exactly the same as given')
        with self.assertRaises(AssertionError, msg='accepted invalid name'):
            GroupStorage(name='abc', description=group_description)
        with self.assertRaises(AssertionError, msg='accepted invalid description'):
            GroupStorage(name=group_name, description='def')
        with self.assertRaises(AssertionError, msg='accepted invalid user'):
            GroupStorage(name=group_name, description=group_description, users=['123'])
        with self.assertRaises(AttributeError, msg='returned id without setting it'):
            str(group_storage)

    def test_group_storage_user_handling(self):
        group_name, group_description, group_storage = self.get_group_storage()
        user_name, user_storage = self.get_user_storage()
        group_storage.add_user(user_storage)
        self.assertEqual(group_storage.users, [user_storage], msg='got different users than given')
        self.assertIs(group_storage.users[0], user_storage, msg='got user that is not exactly the same as given')
        group_storage.add_user(user_storage)
        self.assertEqual(group_storage.users, [user_storage], msg='added already existing user')
        with self.assertRaises(AssertionError, msg='add_user accepted invalid user'):
            group_storage.add_user('abc')
        group_storage.remove_user(user_storage)
        self.assertEqual(group_storage.users, [], msg="didn't remove user")
        with self.assertRaises(AttributeError, msg='removed nonexistent user'):
            group_storage.remove_user(user_storage)

    def tearDown(self) -> None:
        os.remove('picture.jpg')


if __name__ == '__main__':
    unittest.main()
