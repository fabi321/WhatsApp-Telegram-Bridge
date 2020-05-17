from abc import abstractmethod
from io import TextIOWrapper
from threading import Thread
from typing import List

from DBModels.MessageStorage import MessageStorage
from DBModels.TgBotStorage import TgBotStorage
from DBModels.TgGroupStorage import TgGroupStorage
from DBModels.TgUserStorage import TgUserStorage
from Handlers.GeneralStorageManager import GeneralStorageManager
from Utilities.Pipes import Pipes
from Utilities.typings import TgBotId


class TgBotHandler(GeneralStorageManager, Thread):
    def __init__(self, bot_id: TgBotId):
        GeneralStorageManager.__init__(self)
        Thread.__init__(self)
        self.bot_settings: TgBotStorage = self.root.bots[bot_id]
        self.pipe = Pipes(str(self.bot_settings.id))
        self.stop: bool = False

    def __call__(self, *args, **kwargs):
        self.start_bot(*args, **kwargs)

    def run(self, once: bool = False) -> None:
        while True:
            pipe_output: TextIOWrapper = self.pipe.read_pipe
            if not self.handle_pipe_output(str(pipe_output)) or not self.stop:
                self.stop_bot()
                self._connection.close()
                break
            if once:
                break

    def handle_pipe_output(self, pipe_string: str):
        splitted: List[str] = pipe_string.split(':')
        if splitted[0] == 'MessageUser':
            message: MessageStorage = self.root.messages[splitted[1]]
            user: TgUserStorage = self.root.tg_users[splitted[2]]
            self.send_message_to_user(message=message, user=user)
            self.commit()
        elif splitted[0] == 'MessageGroup':
            message: MessageStorage = self.root.messages[splitted[1]]
            group: TgGroupStorage = self.root.tg_groups[splitted[2]]
            self.send_message_to_group(message=message, group=group)
            self.commit()
        elif splitted[0] == 'Quit':
            return False
        else:
            raise KeyError(f'Invalid pipe command sent to {self.bot_settings.id}')
        return True

    def __str__(self):
        return f'{self.bot_settings}'

    def __repr__(self):
        return f'TgBotHandler({self.bot_settings.id!r})'

    @abstractmethod
    def start_bot(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def send_message_to_user(self, message: MessageStorage, user: TgUserStorage):
        raise NotImplementedError()

    @abstractmethod
    def send_message_to_group(self, message: MessageStorage, group: TgGroupStorage):
        raise NotImplementedError()

    @abstractmethod
    def stop_bot(self):
        raise NotImplementedError()
