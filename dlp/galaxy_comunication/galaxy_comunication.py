from os import listdir, system
from os.path import isfile, join

from DLP.settings import STATIC_ROOT
from dlp.file_manager.file_manager import get_site_url, get_galaxy_ip
from dlp.kml_manager.kml_generator import KMLS_PERSISTENT_PATH, \
    KMLS_UPDATES_PATH, KMLS_SLAVE_UPDATES_PATH, KMLS_SLAVE_PERS_PATH
from dlp.models import City

KMLS_TXT_PATH = join(STATIC_ROOT, "kmls/kmls.txt")
KMLS_SLAVE_TXT_PATH = join(STATIC_ROOT, "kmls/kmls_4.txt")
KMLS_URL = "{site_url}{r_path}".format(
    site_url=get_site_url(), r_path="static/kmls/persistent/")
KMLS_URL_UPDATE = "{site_url}{r_path}".format(
    site_url=get_site_url(), r_path="static/kmls/updates/")
KMLS_SLAVE_URL = "{site_url}{r_path}".format(
    site_url=get_site_url(), r_path="static/kmls/slave/persistent/")
KMLS_SLAVE_URL_UPDATE = "{site_url}{r_path}".format(
    site_url=get_site_url(), r_path="static/kmls/slave/updates/")


def sync_kmls_to_galaxy():
    server_path = "/var/www/html"
    system(
        "sshpass -p 'lqgalaxy' scp {kmls_path} lg@{lg_ip}:{lg_path}".format(
            kmls_path=KMLS_TXT_PATH, lg_ip=get_galaxy_ip(),
            lg_path=server_path))
    system(
        "sshpass -p 'lqgalaxy' scp {kmls_path} lg@{lg_ip}:{lg_path}".format(
            kmls_path=KMLS_SLAVE_TXT_PATH, lg_ip=get_galaxy_ip(),
            lg_path=server_path))


def create_kml_file():
    files = [f for f in listdir(KMLS_PERSISTENT_PATH) if
             isfile(join(KMLS_PERSISTENT_PATH, f))]
    updates = [u for u in listdir(KMLS_UPDATES_PATH) if
               isfile(join(KMLS_UPDATES_PATH, u))]
    kml_file = open(KMLS_TXT_PATH, 'w')
    for kml in files:
        kml_file.write("{url}{kml}\n".format(url=KMLS_URL, kml=kml))
    for kml in updates:
        kml_file.write("{url}{kml}\n".format(url=KMLS_URL_UPDATE, kml=kml))
    kml_file.close()
    sync_kmls_slave_file()


def sync_kmls_slave_file():
    files = [f for f in listdir(KMLS_SLAVE_PERS_PATH) if
             isfile(join(KMLS_SLAVE_PERS_PATH, f))]
    updates = [u for u in listdir(KMLS_SLAVE_UPDATES_PATH) if
               isfile(join(KMLS_SLAVE_UPDATES_PATH, u))]
    kml_file = open(KMLS_SLAVE_TXT_PATH, 'w')
    for kml in files:
        kml_file.write("{url}{kml}\n".format(url=KMLS_SLAVE_URL, kml=kml))
    for kml in updates:
        kml_file.write("{url}{kml}\n".format(url=KMLS_SLAVE_URL_UPDATE,
                                             kml=kml))
    kml_file.close()


def start_tour(city):
    city_obj = City.objects.get(id=city)
    message = "echo 'playtour=rotation_{city}' > /tmp/query.txt".format(
        city=city_obj.name
    )
    comunicate(message)


def exit_tour(city):
    city_obj = City.objects.get(id=city)
    message = "echo 'exittour=rotation_{city}' > /tmp/query.txt".format(
        city=city_obj.name
    )
    comunicate(message)


def comunicate(message):
    system("sshpass -p 'lqgalaxy' ssh lg@{lg_ip} \"{message}\"".format(
            message=message, lg_ip=get_galaxy_ip()))


def send_kmls():
    create_kml_file()
    sync_kmls_to_galaxy()
