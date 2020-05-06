from time import sleep
from typing import List

from Utilities.typings import TgMessageId


class MessagePipe(object):
    messages: List[TgMessageId]
    lock: bool = False

    def __init__(self):
        super().__init__()

    def wait_for_message(self) -> TgMessageId:
        if self.lock:
            raise BlockingIOError('Tried to access locked pipe')
        self.lock = True
        while True:
            if len(self.messages) > 0:
                self.lock = False
                return self.messages.pop(0)
            sleep(0.001)

    def send_message(self, message: TgMessageId):
        self.messages.append(message)
