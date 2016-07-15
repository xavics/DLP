from os import listdir, system
from os.path import isfile, join

from DLP.settings import STATIC_ROOT
from dlp.apps import get_site_url, get_galaxy_ip

PERSISTENT_PATH = join(STATIC_ROOT, "kmls/persistent/")
UPDATES_PATH = join(STATIC_ROOT, "kmls/updates/")
KMLS_PATH = join(STATIC_ROOT, "kmls/kmls.txt")
KMLS_URL = "{site_url}{r_path}".format(
    site_url=get_site_url(), r_path="static/kmls/persistent/")
KMLS_URL_UPDATE = "{site_url}{r_path}".format(
    site_url=get_site_url(), r_path="static/kmls/updates/")


def sync_kmls_to_galaxy():
    server_path = "/var/www/html"
    print "sshpass -p 'lqgalaxy' scp {kmls_path} lg@{lg_ip}:{lg_path}".format(
            kmls_path=KMLS_PATH, lg_ip=get_galaxy_ip(), lg_path=server_path)
    system(
        "sshpass -p 'lqgalaxy' scp {kmls_path} lg@{lg_ip}:{lg_path}".format(
            kmls_path=KMLS_PATH, lg_ip=get_galaxy_ip(), lg_path=server_path))
    # File path slave for Logos needed


def create_kml_file():
    files = [f for f in listdir(PERSISTENT_PATH) if
             isfile(join(PERSISTENT_PATH, f))]
    updates = [u for u in listdir(UPDATES_PATH) if
               isfile(join(UPDATES_PATH, u))]
    kml_file = open(KMLS_PATH, 'w')
    for kml in files:
        kml_file.write("{url}{kml}\n".format(url=KMLS_URL, kml=kml))
    for kml in updates:
        kml_file.write("{url}{kml}\n".format(url=KMLS_URL_UPDATE, kml=kml))
    kml_file.close()
    # sync_kmls_slave_file()


def send_kmls():
    create_kml_file()
    sync_kmls_to_galaxy()
