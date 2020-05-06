import os
import sys

from six.moves import configparser


class Config:
    conf_path = os.path.abspath(os.getenv('WAT_CONF', ''))

    if not conf_path or not os.path.isfile(conf_path):
        sys.exit('Could not find configuration file')

    parser = configparser.ConfigParser()
    parser.read(conf_path)

    SETTINGS = {'wa_phone': parser.get('wa', 'phone'), 'wa_password': parser.get('wa', 'password'),
                'owner': parser.getint('tg', 'owner'), 'tg_id': parser.get('tg', 'api_id'),
                'tg_hash': parser.get('tg', 'hash'), 'public_path': parser.get('public', 'path'),
                'public_reachable': parser.get('public', 'address')}
