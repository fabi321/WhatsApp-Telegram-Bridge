# -*- coding: utf-8 -*-
#
# wat-bridge
# https://github.com/rmed/wat-bridge
#
# The MIT License (MIT)
#
# Copyright (c) 2016 Rafael Medina García <rafamedgar@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Signal handlers."""

import sys

from wat_bridge.helper import DataMedia
from wat_bridge.helper import get_contact, get_phone, db_get_group
from wat_bridge.helper import replace_phone_with_name
from wat_bridge.static import SETTINGS, get_logger
from wat_bridge.tg import updater as tgbot
from wat_bridge.wa import wabot

logger = get_logger('signals')


def split_string(text, chars_per_string):
    """
    Splits one string into multiple strings, with a maximum amount of `chars_per_string` characters per string.
    This is very useful for splitting one giant message into multiples.
    :param text: The text to split
    :param chars_per_string: The number of characters per line the text is split into.
    :return: The splitted text as a list of strings.
    """
    return [text[i:i + chars_per_string] for i in range(0, len(text), chars_per_string)]


def sigint_handler(signal, frame):
    """Function used as handler for SIGINT to terminate program."""
    sys.exit(0)


def to_tg_handler(sender, **kwargs):
    """Handle signals sent to Telegram.

    This will involve sending messages through the Telegram bot.

    Args:
        phone (str): Phone number that sent the message.
        message (str): The message received
        media (boolean): True or False
    """
    phone = kwargs.get('phone')
    message = kwargs.get('message')
    media: DataMedia = kwargs.get('media')

    # Check if known contact
    contact = get_contact(phone)
    chat_id = db_get_group(contact)
    if not chat_id:
        chat_id = SETTINGS['owner']

    if media:
        # Media Messages
        type: str = media.get_type()
        path: str = media.get_args()[0]
        caption: str = media.get_kwargs()['caption']
        caption = replace_phone_with_name(caption)
        if type == "image":
            tgbot.bot.send_photo(chat_id, open(path, 'rb'), caption=caption)
        elif type == "video":
            tgbot.bot.send_video(chat_id, open(path, "rb"), caption=caption, supports_streaming=True)
        else:
            tgbot.bot.send_document(chat_id, open(path, 'rb'), caption=caption)
    else:
        message = replace_phone_with_name(message)
        # Text Messages
        if not contact:
            # Unknown sender
            output = 'Message from #unknown\n'
            output += 'Phone number: %s\n' % phone
            output += '---------\n'
            output += message

            logger.info('received message from unknown number: %s' % phone)

        else:
            group = db_get_group(contact)
            if not group:
                # Known sender
                output = 'Message from #%s\n' % contact
                output += '---------\n'
                output += message
            else:
                # Contact is bound to group
                chat_id = group
                output = message

            logger.info('received message from %s' % contact)

        # Deliver message through Telegram
        for chunk in split_string(output, 3000):
            tgbot.bot.send_message(chat_id, chunk)


def to_wa_handler(sender, **kwargs):
    """Handle signals sent to Whatsapp.

    This will involve sending messages through the Whatsapp bot.

    Args:
        contact (str): Name of the contact to send the message to.
        message (str): The message to send
    """
    contact = kwargs.get('contact')
    message = kwargs.get('message')
    media = kwargs.get('media')

    # Check if known contact
    phone = get_phone(contact)

    if not phone:
        # Abort
        tgbot.bot.send_message(
            SETTINGS['owner'],
            'Unknown contact: "%s"' % contact
        )

        return

    logger.info('sending message to %s (%s)' % (contact, phone))

    wabot.send_msg(phone=phone, message=message, media=media)
