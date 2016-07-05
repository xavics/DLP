from __future__ import unicode_literals

import os
from DLP.settings import BASE_DIR
from django.apps import AppConfig


class DlpConfig(AppConfig):
    name = 'dlp'
    verbose_name = 'Drone Logistics Platform'


def get_site_url():
    f = open(os.path.join(BASE_DIR + "/ipsettings"), 'r')
    ip_config = f.read().split(',')
    f.close()
    return ip_config[1]


def get_galaxy_ip():
    f = open(os.path.join(BASE_DIR + "/ipsettings"), 'r')
    ip_config = f.read().split(',')
    f.close()
    return ip_config[0]
