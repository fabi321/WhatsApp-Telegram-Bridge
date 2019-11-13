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

"""Code for the Telegram side of the bridge."""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update, Message
import telegram
import time
from wat_bridge.helper import *
from wat_bridge.static import SETTINGS, SIGNAL_WA, get_logger
from wat_bridge.wa import wabot

logger = get_logger('tg')

# Create handlers

def start(update: Update, context: CallbackContext):
    """Show usage of the bot.

    Args:
        message: Received Telegram message.
    """
    response = ('Source Code available here: https://github.com/SpEcHiDe/wat-bridge \r\n'
		'Please read https://blog.shrimadhavuk.me/posts/2017/12/31/Telegram-WhatApp/ to know how to use the bot! \r\n'
		'Terms and Consitions: https://backend.shrimadhavuk.me/TermsAndConditions \r\n'
		'Privacy Policy: https://backend.shrimadhavuk.me/PrivacyPolicy \r\n'
		'\r\n New Year Hobby Project by @rmedgar, @SpEcHlDe, @SubinSiby, and many more .. \r\n'
               )

    update.message.reply_text(response)

def me(update: Update, context: CallbackContext):
    """Get user ID.

    Args:
        message: Received Telegram message.
    """
    update.message.reply_text(update.message.chat.id)

def add_contact(update: Update, context: CallbackContext):
    """Add a new Whatsapp contact to the database.

    Message has the following format:

        /add <name> <phone>

    Args:
        message: Received Telegram message.
    """
    if update.message.chat.id != SETTINGS['owner']:
        update.message.reply_text('You are not the owner of this bot')
        return

    # Get name and phone
    args = update.message.text
    try:
        dump, name, phone = args.split(' ', 2)

        # Check if it already exists
        if get_contact(phone) or get_phone(name):
            update.message.reply_text('A contact with those details already exists')
            return

        # Add to database
        db_add_contact(name, phone)

        update.message.reply_text('Contact added')

    except:
        update.message.reply_text('Syntax: /add <name> <phone>')
        return


def bind(update: Update, context: CallbackContext):
    """Bind a contact to a group.

    Message has the following format:

        /bind <name> <group id>

    Args:
        message: Received Telegram message.
    """
    if update.message.chat.id != SETTINGS['owner']:
        update.message.reply_text('You are not the owner of this bot')
        return

    # Get name and phone
    args = update.message.text
    try:
        dump, name, group_id = args.split(' ', 2)

        group_id = safe_cast(group_id, int)
        if not group_id:
            update.message.reply_text('Group id has to be a number')
            return

        # Ensure contact exists
        if not get_phone(name):
            update.message.reply_text('No contact found with that name')
            return

        # Check if it already exists
        current = db_get_contact_by_group(group_id)
        if current:
            update.message.reply_text('This group is already bound to ' + current)
            return

        # Add to database
        db_set_group(name, group_id)

        update.message.reply_text('Bound to group')
    except:
        update.message.reply_text('Syntax: /bind <name> <group id>')
        return


def unbind(update: Update, context: CallbackContext):
    """Unbind a contact from his group.

    Message has the following format:

        /unbind <name>

    Args:
        message: Received Telegram message.
    """
    if update.message.chat.id != SETTINGS['owner']:
        update.message.reply_text('You are not the owner of this bot')
        return

    # Get name and phone
    name = cut(update.message.text)

    if not name:
        update.message.reply_text('Syntax: /unbind <name>')
        return

    # Ensure contact exists
    if not get_phone(name):
        update.message.reply_text('No contact found with that name')
        return

    # Check if it already exists
    group = db_get_group(name)
    if not group:
        update.message.reply_text('Contact was not bound to a group')
        return

    # Add to database
    db_set_group(name, None)

    update.message.reply_text('Unbound from group')

def blacklist(update: Update, context: CallbackContext):
    """Blacklist a Whatsapp phone.

    Message has the following format:

        /blacklist
        /blacklist <phone>

    Note that if no phone is provided, a list of blacklisted phone is returned.

    Args:
        message: Received Telegram message.
    """
    if update.message.chat.id != SETTINGS['owner']:
        update.message.reply_text('you are not the owner of this bot')
        return

    # Get phone
    phone = cut(update.message.text)

    if not phone:
        # Return list
        blacklist = get_blacklist()

        response = 'Blacklisted phones:\n\n'
        for b in blacklist:
            response += '- %s\n' % b

        update.message.reply_text(response)
        return

    # Blacklist a phone
    if is_blacklisted(phone):
        # Already blacklisted
        update.message.reply_text('That phone is already blacklisted')
        return

    db_add_blacklist(phone)

    update.message.reply_text('Phone has been blacklisted')

def list_contacts(update: Update, context: CallbackContext):
    """List stored contacts.

    Message has the following format:

        /contacts

    Args:
        message: Received Telegram message.
    """
    if update.message.chat.id != SETTINGS['owner']:
        update.message.reply_text('you are not the owner of this bot')
        return

    contacts = db_list_contacts()
    g = 0
    response = 'Contacts:\n'
    for c in contacts:
        response += '- %s (%s)' % (c[0], c[1])
        if c[2]:
            response += ' -> group %s' % c[2]
            g = g + 1
        response += '\n'
    response += str(len(contacts)) + " Contacts in " + str(g) + ' Groups'

    update.message.reply_text(response)

def rm_contact(update: Update, context: CallbackContext):
    """Remove a Whatsapp contact from the database.

    Message has the following format:

        /rm <name>

    Args:
        message: Received Telegram message.
    """
    if update.message.chat.id != SETTINGS['owner']:
        update.message.reply_text('you are not the owner of this bot')
        return

    # Get name
    name = cut(update.message.text)

    if not name:
        update.message.reply_text('Syntax: /rm <name>')
        return

    # Check if it already exists
    if not get_phone(name):
        update.message.reply_text('No contact found with that name')
        return

    # Add to database
    db_rm_contact(name)

    update.message.reply_text('Contact removed')

def relay_wa(update: Update, context: CallbackContext):
    """Send a message to a contact through Whatsapp.

    Message has the following format:

        /send <name> <message>

    Args:
        message: Received Telegram message.
    """
    #if update.message.chat.id != SETTINGS['owner']:
    #    update.message.reply_text('you are not the owner of this bot')
    #    return

    # Get name and message
    args = update.message.text
    try:
        _, name, text = args.split(' ', 2)

        # Relay
        logger.info('relaying message to Whatsapp')
        SIGNAL_WA.send('tgbot', contact=name, message=text)
    except:
        update.message.reply_text('Syntax: /send <name> <message>')
        return

def unblacklist(update: Update, context: CallbackContext):
    """Unblacklist a Whatsapp phone.

    Message has the following format:

        /unblacklist <phone>

    Args:
        message: Received Telegram message.
    """
    if update.message.chat.id != SETTINGS['owner']:
        update.message.reply_text('you are not the owner of this bot')
        return

    # Get phone
    phone =cut(update.message.text)

    if not phone:
        # Return list
        update.message.reply_text('Syntax: /unblacklist <phone>')
        return

    # Unblacklist a phone
    if not is_blacklisted(phone):
        # Not blacklisted
        update.message.reply_text('That phone is not blacklisted')
        return

    db_rm_blacklist(phone)

    update.message.reply_text('Phone has been unblacklisted')

def link(update: Update, context: CallbackContext):
    """Link a WhatsApp group

    Message has the following format:

        /link <group_id>

    Args:
        message: Received Telegram message.
    """
    if update.message.chat.type not in ['group', 'supergroup']:
        update.message.reply_text('This operation can be done only in a group')
        return

    # Get name and message
    wa_group_id = cut(update.message.text)
    wa_group_name = wa_id_to_name(wa_group_id)

    if not wa_group_id:
        update.message.reply_text('Syntax: /link <groupID>')
        return

    # Add to database
    db_add_contact(wa_group_name, wa_group_id)

    # Add to database
    db_set_group(wa_group_name, update.message.chat.id)

    update.message.reply_text('Bridge Connected. Please subscribe to @WhatAppStatus for the bridge server informations. \r\n While this service is free, I still have to pay for the servers, so please consider becoming a supporter at https://buymeacoff.ee/SpEcHiDe \r\n This message won\'t appear again! Enjoy the \'free\' service!!')

def unlink(update: Update, context: CallbackContext):
    """Unlink bridge

    Message has the following format:

        /unlink

    Args:
        message: Received Telegram message.
    """
    if update.message.chat.type not in ['group', 'supergroup']:
        update.message.reply_text('This operation can be done only in a group')
        return

    # Check if it already exists
    wa_group_name = db_get_contact_by_group(update.message.chat.id)
    if not wa_group_name:
        update.message.reply_text('This group is not bridged to anywhere')
        return

    # Add to database
    db_rm_contact(wa_group_name)

    update.message.reply_text('Bridge has been successfully removed.')

def bridge_on(update: Update, context: CallbackContext):
    """Turn on bridge

    Message has the following format:

        /bridgeOn

    Args:
        message: Received Telegram message.
    """
    if update.message.chat.type not in ['group', 'supergroup']:
        update.message.reply_text('This operation can be done only in a group')
        return

    # Check if it already exists
    wa_group_name = db_get_contact_by_group(update.message.chat.id)
    if not wa_group_name:
        update.message.reply_text('This group is not bridged to anywhere')
        return

    db_toggle_bridge_by_tg(update.message.chat.id, True)

    update.message.reply_text('Bridge has been turned on.')

def bridge_off(update: Update, context: CallbackContext):
    """Turn off bridge temporarily

    Message has the following format:

        /bridgeOff

    Args:
        message: Received Telegram message.
    """
    if update.message.chat.type not in ['group', 'supergroup']:
        update.message.reply_text('This operation can be done only in a group')
        return

    # Check if it already exists
    wa_group_name = db_get_contact_by_group(update.message.chat.id)
    if not wa_group_name:
        update.message.reply_text('This group is not bridged to anywhere')
        return

    db_toggle_bridge_by_tg(update.message.chat.id, False)

    update.message.reply_text('Bridge has been turned off. Use `/bridgeOn` to turn it back on')

#@tgbot.message_handler(func=lambda message: update.message.chat.type in ['group', 'supergroup'])
def relay_group_wa(update: Update, context: CallbackContext):
    """ Send a message received in a bound group to the correspondending contact through Whatsapp.

    Args:
        message: Received Telegram message.
    """

    if update.message.text in ['/jc', '/joincall']:
        meet_jit_si_NEW_call_h(update, context)
        return

    cid = update.message.chat.id

    if not db_is_bridge_enabled_by_tg(cid):
        return

    uid = update.message.from_user.id
    text = "<" + update.message.from_user.first_name + ">: " + update.message.text

    #if uid != SETTINGS['owner']:
    #    update.message.reply_text('you are not the owner of this bot')
    #    return

    name = db_get_contact_by_group(group=cid)
    if not name:
        logger.info('no user is mapped to this group')
        #update.message.reply_text('no user is mapped to this group')
        return

    # Relay
    logger.info('relaying message to Whatsapp')
    SIGNAL_WA.send('tgbot', contact=name, message=text)

def meet_jit_si_NEW_call_h(update: Update, context: CallbackContext):
    logger.debug('NEW pending feature')
    cid = update.message.chat.id
    name = db_get_contact_by_group(group=cid)
    reply_message = "Click on this link to join a @GroupCall with all the users. \r\n"
    if not name:
        reply_message = "This group is not bridged to anywhere. PLEASE DO NOT ABUSE THIS FREE SERVICE."
    else:
        reply_message += "https://meet.jit.si/" + "" + wa_id_to_name(name + str(round(time.time())) + name)
    update.message.reply_text(reply_message)
    if name:
        SIGNAL_WA.send('tgbot', contact=name, message=reply_message)

def get_reason_string(message: Message) -> str:
    reason: str = ''
    if message.animation or message.game or message.poll:
        reason += "Whatsapp hasn't implemented this yet"
    elif message.audio or message.sticker or message.photo or message.contact or message.document\
            or message.video or message.video_note or message.location:
        reason += "The bridge hasn't implemented this yet"
    return reason

def get_type_string(message: Message) -> str:
    if message.animation:
        return 'video'
    elif message.contact:
        return 'contact'
    elif message.document:
        return 'document'
    elif message.game:
        return 'game'
    elif message.location:
        return 'location'
    elif message.video or message.video_note:
        return 'video'
    elif message.poll:
        return 'poll'
    elif message.audio or message.voice:
        return 'audio'
    elif message.sticker:
        return 'sticker'
    elif message.photo:
        return 'photo'
    return 'other_type'

# Handles all sent documents and audio files
#@tgbot.message_handler(
#    content_types=['document', 'audio', 'photo', 'sticker', 'video',
#                   'voice', 'video_note', 'contact', 'location'])
def handle_docs_audio(update: Update, context: CallbackContext):
    """ Handle media messages received in Telegram
    """
    # print(message)
    cid = update.message.chat.id

    if not db_is_bridge_enabled_by_tg(cid):
        return

    name = db_get_contact_by_group(group=cid)
    if not name:
        logger.info('no user is mapped to this group')
        #update.message.reply_text('no user is mapped to this group')
        return
#    elif message.contact
#            or message.location:

    reason = None
    caption = update.message.caption
    attachment = update.message.effective_attachment
    if not attachment:# and any([isinstance(attachment, i) for i in [telegram.Video, telegram.Audio, telegram.Document, telegram.VideoNote, telegram.Voice, telegram.Sticker, telegram.Animation]]):
        if attachment.file_size < 16 * 10**6:
            file: telegram.File = attachment.get_file()
            path: str = './DOWNLOADS/' + attachment.file_id + '.' + attachment.mime_type.split('/')[1]
            file.download(custom_path=path)
            logger.info('relaying media message to Whatsapp')
            try:
                media: DataMedia = DataMedia(path, get_type_string(update.message), attachment.caption)
            except:
                media: DataMedia = DataMedia(path, get_type_string(update.message))
            SIGNAL_WA.send('tgbot', contact=name, media=media)
            return
        else:
            reason = 'The Media is too large for Whatsapp'
    elif not attachment:# and isinstance(attachment, telegram.PhotoSize):
        for i in attachment:
            if attachment.size < 16 * 10 ** 6:
                file: telegram.File = attachment.get_file()
                path: str = './DOWNLOADS/' + attachment.file_id + '.' + attachment.mime_type.split('/')[1]
                file.download(custom_path=path)
                logger.info('relaying media message to Whatsapp')
                try:
                    media: DataMedia = DataMedia(path, get_type_string(update.message), attachment.caption)
                except:
                    media: DataMedia = DataMedia(path, get_type_string(update.message))
                SIGNAL_WA.send('tgbot', contact=name, media=media)
                return
            else:
                reason = 'The Media is too large for Whatsapp'
    elif attachment and isinstance(attachment, telegram.Contact):
        contact: telegram.Contact = attachment
        vcard: str = contact.vcard
        return
    elif attachment and isinstance(attachment, telegram.Location):
        location: telegram.Location = attachment
        media: Location = Location(location.longitude, location.latitude)
        logger.info('relaying location to Whatsapp')
        SIGNAL_WA.send('tgbot', contact=name, media=media)
        return
    elif attachment:
        reason = get_reason_string(update.message)
    if reason:
        name = db_get_contact_by_group(group=cid)
        type = get_type_string(update.message)
        if not name:
            logger.info('no user is mapped to this group')
            #update.message.reply_text('no user is mapped to this group')
            return
        if not caption:
            caption = ''
        link = "https://telegram.dog/dl"
        if update.message.chat.type == 'group':
            link = 'https://t.me/' + update.message.chat.id
        elif update.message.chat.type == 'supergroup':
            link = update.message.link

        text = " " + update.message.from_user.first_name + " sent you " + type + \
	       " with caption " + caption + \
    	   ". \nsadly this is not supported bechause " + reason+ \
            "\nIf you want to view this, go to " + link + " or create your own account."
        # print(text)
        logger.info('relaying sorry message to Whatsapp')
        SIGNAL_WA.send('tgbot', contact=name, message=text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s, in Chat %s"', update, context.error, context.chat_data)

"""Start the bot."""
# Create the Updater and pass it your bot's token.
# Make sure to set use_context=True to use the new context based callbacks
# Post version 12 this will no longer be necessary
updater = Updater(SETTINGS['tg_token'], use_context=True)

# Get the dispatcher to register handlers
dp = updater.dispatcher

# on different commands - answer in Telegram
dp.add_handler(CommandHandler("start", help))
dp.add_handler(CommandHandler("help", help))
dp.add_handler(CommandHandler("me", me))
dp.add_handler(CommandHandler("add", add_contact))
dp.add_handler(CommandHandler("bind", bind))
dp.add_handler(CommandHandler("unbind", unbind))
dp.add_handler(CommandHandler("blacklist", blacklist))
dp.add_handler(CommandHandler("contacts", list_contacts))
dp.add_handler(CommandHandler("rm", rm_contact))
dp.add_handler(CommandHandler("send", relay_wa))
dp.add_handler(CommandHandler("unblacklist", unblacklist))
dp.add_handler(CommandHandler("link", link))
dp.add_handler(CommandHandler("unlink", unlink))
dp.add_handler(CommandHandler("bridgeOn", bridge_on))
dp.add_handler(CommandHandler("bridgeOff", bridge_off))

# on noncommand i.e message - echo the message on Telegram
dp.add_handler(MessageHandler(Filters.photo, handle_docs_audio))
dp.add_handler(MessageHandler(Filters.video_note, handle_docs_audio))
dp.add_handler(MessageHandler(Filters.video, handle_docs_audio))
dp.add_handler(MessageHandler(Filters.voice, handle_docs_audio))
dp.add_handler(MessageHandler(Filters.sticker, handle_docs_audio))
dp.add_handler(MessageHandler(Filters.location, handle_docs_audio))
dp.add_handler(MessageHandler(Filters.game, handle_docs_audio))
dp.add_handler(MessageHandler(Filters.document, handle_docs_audio))
dp.add_handler(MessageHandler(Filters.contact, handle_docs_audio))
dp.add_handler(MessageHandler(Filters.audio, handle_docs_audio))
dp.add_handler(MessageHandler(Filters.animation, handle_docs_audio))
dp.add_handler(MessageHandler(Filters.group, relay_group_wa))

# log all errors
dp.add_error_handler(error)

# Start the Bot
updater.start_polling()

# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
#updater.idle()