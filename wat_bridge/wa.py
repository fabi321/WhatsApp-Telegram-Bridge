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

"""Code for the Whatsapp side of the bridge."""

import base64
import traceback
import time
import mimetypes

from yowsup.layers import YowLayerEvent
from yowsup.layers.interface import ProtocolEntityCallback
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity, ExtendedTextMessageProtocolEntity
from yowsup.stacks import YowStackBuilder
from yowsup.layers.protocol_media.protocolentities import *
from yowsup.demos.cli.layer import YowsupCliLayer
from yowsup.demos.common.sink_worker import SinkWorker
from yowsup.layers.protocol_media.mediacipher import MediaCipher
from yowsup.profile.profile import YowProfile
from yowsup.config.manager import ConfigManager

from wat_bridge.static import *
from wat_bridge.helper import *

logger = get_logger('wa')

class WaLayer(YowsupCliLayer):
    """Defines the yowsup layer for interacting with Whatsapp."""

    def __init__(self):
        super().__init__()
        self.presence_name('Warping to Telegram')
        self.profile_setStatus('Wants to go back to Telegram')

    @ProtocolEntityCallback('message')
    def on_message(self, message:TextMessageProtocolEntity):
        try:
            """Received a message."""
            # Parse information
            sender = message.getFrom(full=False)
            oidtotg = message.getFrom(full=True)

            logger.debug('received message from %s' % oidtotg)

            # Send receipt
            self.toLower(message.ack(self.sendRead))

            # https://github.com/tgalal/yowsup/issues/1411#issuecomment-203419530
            # if isinstance(type(message), unicode) :
            # message = message.encode('utf-8')
            # entity = TextMessageProtocolEntity(message, sender)
            # self.toLower(entity)

            if not sender:
                logger.warning('Empty sender')
                return

            # Do stuff
            if is_blacklisted(sender):
                logger.debug('phone is blacklisted: %s' % sender)
                return

            participant = message.getParticipant()
            if participant:
                participant = participant.strip("@g.us")
            else:
                participant = sender
            if participant.find('@s.whatsapp.net') >= 0:
                participant = participant.strip('@s.whatsapp.net')

            contact_name = get_contact(participant)

            if not contact_name:
                contact_name = message.notify + "-" + participant

            # body = "<" + oidtotg + ">: " + message.getBody()
            # body = "NULL"
            if message.getType() == "text":
                logger.debug("is text message")
                if isinstance(message, TextMessageProtocolEntity):
                    body = message.getBody()
                elif isinstance(message, ExtendedTextMessageProtocolEntity):
                    body = message.text
                else:
                    logger.debug(str(message) + str(type(message)))
                    body = "Internal error"

                if body == '/getID' or body == '/link':
                    self.send_msg(phone=sender, message="/link " + sender)

                    HelpInstructions = "Please send the above message in the Telegram group that you would like to bridge!"
                    self.send_msg(phone=sender, message=HelpInstructions)
                    # self.send_msg(phone=sender, message="new registrations are closed. please contact https://youtu.be/9r-yzKfL8xw for bridging Telegram ")
                    return
                elif body[0:5] == '/add ':
                    if participant == sender:
                        name = body[5:]
                        if not name:
                            ReplyMessage = "Syntax: /add <name>"
                        else:
                            if contact_name:
                                db_rm_contact(contact_name)
                                db_add_contact(name, sender)
                                ReplyMessage = "name already existed. name removed and added. Pleae verify with ```/me```"
                            else:
                                db_add_contact(name, sender)
                                ReplyMessage = "name added. Pleae verify with ```/me```"
                        self.send_msg(phone=sender, message=ReplyMessage)
                        return
                elif body == '/me':
                    if not contact_name:
                        ReplyMessage = "Please send ```/add NAME``` to add you to my contacts."
                    else:
                        ReplyMessage = "I have saved your name as " + contact_name + ". You can edit your name in my contacts by sending ```/add NAME```!"
                    if participant == sender:
                        self.send_msg(phone=sender, message=ReplyMessage)
                        return
                elif body == '/bridgeOn':
                    toggle = db_toggle_bridge_by_wa(sender, True)

                    if toggle is None:
                        Message = 'This group is not bridged to anywhere. Use ```/link``` to start bridging.'
                    else:
                        Message = 'Bridge has been turned on!'

                    self.send_msg(phone=sender, message=Message)

                    return

                elif body == '/bridgeOff':
                    toggle = db_toggle_bridge_by_wa(sender, False)

                    if toggle is None:
                        Message = 'This group is not bridged to anywhere. Use ```/link``` to start bridging.'
                    else:
                        Message = 'Bridge has been turned off. Use ```/bridgeOn``` to turn it back on.'

                    self.send_msg(phone=sender, message=Message)

                    return

                if not db_is_bridge_enabled_by_wa(sender) and message.isGroupMessage():
                    return

                logger.info("prefix WHO send this message, to message")
                TheRealMessageToSend = "<#" + contact_name + ">: " + body

                # Relay to Telegram
                logger.info('relaying message to Telegram')
                SIGNAL_TG.send('wabot', phone=sender, message=TheRealMessageToSend)

            if message.getType() == "media":
                if isinstance(message, DownloadableMediaMessageProtocolEntity):
                    filepath = download.download(message)
                    TheRealMessageToSend = message.media_type + ': <#' + contact_name + '>'
                    if isinstance(message, (VideoDownloadableMediaMessageProtocolEntity, ImageDownloadableMediaMessageProtocolEntity)) and message.caption and message.caption != '':
                        TheRealMessageToSend += ': ' + message.caption
                    media_message = DataMedia(filepath, message.media_type, TheRealMessageToSend)
                    # Relay to Telegram
                    logger.info('relaying message to Telegram')
                    SIGNAL_TG.send('wabot', phone=sender, media=media_message)
        except Exception as x:
            traceback.print_exc()

    def send_msg(self, **kwargs):
        """Send a message.

        Arguments:
            phone (str): Phone to send the message to.
            message (str): Message to send, empty when media
            media (Media): Media to send
        """
        phone = kwargs.get('phone')

        if not phone:
            return

        message = kwargs.get('message')

        while not self.connected:
            logger.info('Waiting for WA to log in before relaying message')
            time.sleep(1)

        if phone.find('/link ') == 0:
            phone = phone.replace('/link ', '', 1)
        if message:
            message = message.encode('utf8')
            self.message_send(phone, message)

        media: Media = kwargs.get('media')

        if isinstance(media, DataMedia):
            self.media_send(phone, *media.get_args(), **media.get_kwargs())

        elif isinstance(media,  Location):
            self.location(phone, *media.get_args(), **media.get_kwargs())

    @ProtocolEntityCallback("notification")
    def onNotification(self, notification):
        notificationData = notification.__str__()
        if notificationData:
            self.output(notificationData, tag = "Notification")
        else:
            SIGNAL_TG.send('wabot', message="From :%s, Type: %s" % (self.jidToAlias(notification.getFrom()), notification.getType()), tag = "Notification")



class Download(SinkWorker):
    def __init__(self, storage_dir):
        super(Download, self).__init__(storage_dir)

    def download(self, media_message_protocolentity: MediaMessageProtocolEntity):
        if media_message_protocolentity is None:
            return None
        if isinstance(media_message_protocolentity, DownloadableMediaMessageProtocolEntity):
            logger.info(
                "Processing [url=%s, media_key=%s]" %
                (media_message_protocolentity.url, base64.b64encode(media_message_protocolentity.media_key))
            )
        else:
            logger.info("Processing %s" % media_message_protocolentity.media_type)

        filedata = None
        fileext = None
        if isinstance(media_message_protocolentity, ImageDownloadableMediaMessageProtocolEntity):
            media_info = MediaCipher.INFO_IMAGE
            filename = "image"
        elif isinstance(media_message_protocolentity, AudioDownloadableMediaMessageProtocolEntity):
            media_info = MediaCipher.INFO_AUDIO
            filename = "ptt" if media_message_protocolentity.ptt else "audio"
        elif isinstance(media_message_protocolentity, VideoDownloadableMediaMessageProtocolEntity):
            media_info = MediaCipher.INFO_VIDEO
            filename = "video"
        elif isinstance(media_message_protocolentity, DocumentDownloadableMediaMessageProtocolEntity):
            media_info = MediaCipher.INFO_DOCUM
            filename = media_message_protocolentity.file_name
        elif isinstance(media_message_protocolentity, ContactMediaMessageProtocolEntity):
            filename = media_message_protocolentity.display_name
            filedata = media_message_protocolentity.vcard
            fileext = "vcard"
        elif isinstance(media_message_protocolentity, StickerDownloadableMediaMessageProtocolEntity):
            media_info = MediaCipher.INFO_IMAGE
            filename = "sticker"
            fileext = "webp"
        else:
            logger.error("Unsupported Media type: %s" % media_message_protocolentity.__class__)
            return None

        if filedata is None:
            enc_data = self._download(media_message_protocolentity.url)
            if enc_data is None:
                logger.error("Download failed")
                return None

            filedata = self._decrypt(enc_data, media_message_protocolentity.media_key, media_info)
            if filedata is None:
                logger.error("Decrypt failed")
                return None

        if fileext is None:
            fileext = mimetypes.guess_extension(media_message_protocolentity.mimetype).replace('.', '', 1)
        filename_full = "%s.%s" % (filename, fileext)
        filepath = self._create_unique_filepath(os.path.join(self._storage_dir, filename_full))
        if self._write(filedata, filepath):
            logger.info("Wrote %s" % filepath)
            return filepath
        else:
            return None

if not os.path.exists("./DOWNLOADS"):
    os.makedirs("./DOWNLOADS")
download = Download('./DOWNLOADS/')

profile: YowProfile = YowProfile(SETTINGS['wa_phone'])

# Prepare stack
wabot = WaLayer()

_connect_signal = YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT)

WA_STACK = (
    YowStackBuilder()
	.pushDefaultLayers()
	# .pushDefaultLayers(False)
	.push(wabot)
	.build()
)

#SETTINGS['wa_password']
config_manager = ConfigManager()
WA_STACK.setProfile(profile)

