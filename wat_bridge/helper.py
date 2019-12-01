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

"""Helper functions."""

import urllib.request
import shutil
import hashlib
import os
from wat_bridge.static import DB, CONTACT
from yowsup.layers.protocol_media.protocolentities.iq_requestupload import RequestUploadIqProtocolEntity
from typing import List, Dict

def db_add_blacklist(phone):
    """Add a new blacklisted phone to the database.

    Args:
        phone (str): Phone of the contact.

    Returns:
        ID of the inserted element.
    """
    return DB.insert({'name': None, 'phone': phone, 'blacklisted': True, 'group': None})

def db_add_contact(name, phone):
    """Add a new contact to the database.

    Args:
        name (str): Name to use for the contact.
        phone (str): Phone of the contact.

    Returns:
        ID of the inserted element.
    """
    return DB.insert({'name': name.lower(), 'phone': phone, 'blacklisted': False, 'group': None, 'enabled': True})

def db_list_contacts():
    """Obtain a list of contacts.

    The list contains tuples with (name, phone)

    Returns:
        List of tuples
    """
    result = DB.search(CONTACT.blacklisted == False)

    return [(a['name'], a['phone'], a.get('group')) for a in result]

def db_rm_blacklist(phone):
    """Removes a blacklisted phone from the database.

    Args:
        phone (str): Phone of the contact.
    """
    DB.remove((CONTACT.phone == phone) & (CONTACT.blacklisted == True))

def db_rm_contact(name):
    """Remove a contact from the the database.

    Args:
        name (str): Name of the contact to remove.
    """
    DB.remove(CONTACT.name == name.lower())

def get_blacklist():
    """Obtain a list of blacklisted phones.

    Returns:
        List of strings.
    """
    result = DB.search(CONTACT.blacklisted == True)

    if not result:
        return []

    return [a['phone'] for a in result]

def get_contact(phone):
    """Get contact name from a phone number.

    Args:
        phone (str): Phone to search.

    Returns:
        String with the contact name or `None` if not found.
    """
    result = DB.get((CONTACT.phone == phone) & (CONTACT.blacklisted == False))

    if not result:
        return None

    return result['name']

def get_phone(contact):
    """Get phone number from a contact name.

    Args:
        contact (str): Name assigned to the contact

    Returns:
        String with the phone number or `None` if not found.
    """
    result = DB.get((CONTACT.name == contact.lower()) & (CONTACT.blacklisted == False))

    if not result:
        return None

    return result['phone']

def is_blacklisted(phone):
    """Check if a phone number is blacklisted.

    Args:
        phone (str): Phone to check

    Returns:
        True or False
    """
    result = DB.get((CONTACT.phone == phone) & (CONTACT.blacklisted == True))

    if not result:
        return False

    return True

def db_get_group(contact):
    result = DB.get((CONTACT.name == contact.lower()))

    if not result:
        return None

    # return None for backward compatibility if there is no group column
    return result.get('group')

def db_set_group(contact, group):
    DB.update({'group': group}, (CONTACT.name == contact.lower()))

def db_set_phone(contact, phone):
    DB.update({'phone': phone}, (CONTACT.name == contact.lower()))

def db_toggle_bridge_by_tg(group, toggle):
    result = DB.get((CONTACT.group == group))

    if not result:
        return None

    DB.update({'enabled': toggle}, (CONTACT.group == group))

    return toggle

def db_toggle_bridge_by_wa(phone, toggle):
    result = DB.get((CONTACT.phone == phone))

    if not result:
        return None

    DB.update({'enabled': toggle}, (CONTACT.phone == phone))

    return toggle

def db_is_bridge_enabled_by_tg(group):
    result = DB.get((CONTACT.group == group))

    if not result:
        return None

    return result.get('enabled')

def db_is_bridge_enabled_by_wa(phone):
    result = DB.get((CONTACT.phone == phone))

    if not result:
        return None

    return result.get('enabled')

def db_get_contact_by_group(group):
    """Get phone number from a group id.

    Args:
        group (int): Group id assigned to the contact.

    Returns:
        String with the phone number or `None` if not found.
    """
    result = DB.get((CONTACT.group == group))

    if not result:
        return None

    return result['name']

def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default

def wa_id_to_name(val):
    if val:
        return hashlib.md5(str(val).encode('utf-8')).hexdigest()
    else:
        return None

class Media:
    def __init__(self, type: str):
        self._type: str = type

    def get_type(self) -> str:
        return self._type

    def get_args(self) -> List[object]:
        pass

    def get_kwargs(self) -> Dict[str, str]:
        pass


class DataMedia(Media):
    def __init__(self, location: str, type: str, caption: str = None):
        if location not in RequestUploadIqProtocolEntity.TYPES_MEDIA:
            pass
        self._location: str = location
        self._caption: str = caption
        Media.__init__(self, type)

    def get_args(self) -> List[str]:
        return [self._location, self._type]

    def get_kwargs(self) -> Dict[str, str]:
        return {'caption': self._caption}


class Location(Media):
    def __init__(self, long: float, lat: float, name: str=None, address: str=None, url: str=None):
        Media.__init__(self, 'location')
        self._long: float = long
        self._lat: float = lat
        self._name: str = name
        self._address: str = address
        self._url: str = url

    def get_args(self) -> List[float]:
        return [self._lat, self._long]

    def get_kwargs(self) -> Dict[str, str]:
        return {'name': self._name, 'address': self._address, 'url': self._url}

def cut(message: str) -> str:
    _, out = message.split(' ', 1)
    return out

def create_unique_filepath(filepath):
    file_dir = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    result_filename = filename
    dissected = os.path.splitext(filename)
    count = 0
    while os.path.exists(os.path.join(file_dir, result_filename)):
        count += 1
        result_filename = "%s_%d%s" % (dissected[0], count, dissected[1])

    return os.path.join(file_dir, result_filename)


def secure_phone_number(phone: str) -> str:
    # Check if is starts with +
    if phone.find('+') == 0:
        phone = phone.replace('+', '', count=1)

    # Check if it contains anything exept numbers for eac segment
    for i in phone.split('-'):
        if not i.isnumeric():
            return ''
    return phone

def replace_phone_with_name(message: str) -> str:
    new_messaage: str = ''
    for i in message.split('@'):
        if secure_phone_number(i.split()[0]) == '':
            new_messaage += '@' + i
        else:
            contact_name = get_contact(i.split()[0])
            new_messaage += '<' + ('#' + contact_name if contact_name else '@' + i.split()[0]) + '>'
            for j in range(1, len(i.split())):
                new_messaage += ' ' + i.split()[j]
    return new_messaage[1:]

