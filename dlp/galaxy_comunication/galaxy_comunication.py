from os import listdir, system
from os.path import isfile, join, dirname, abspath

from dlp.apps import get_site_url, get_galaxy_ip

persistent_path = abspath(
    join(dirname(__file__), "..")) + "/static/kmls/persistent/"
updates_path = abspath(
    join(dirname(__file__), "..")) + "/static/kmls/updates/"
kmls_path = abspath(
    join(dirname(__file__), "..")) + "/static/kmls/kmls.txt"
kmls_url = get_site_url() + "static/kmls/persistent/"
kmls_url_upd = get_site_url() + "static/kmls/updates/"
GALAXY_IP = get_galaxy_ip()


def sync_kmls_to_galaxy():
    server_path = "/var/www/html"
    print "sshpass -p 'lqgalaxy' scp " + kmls_path + " lg@" + GALAXY_IP +\
          ":" + server_path
    system(
        "sshpass -p 'lqgalaxy' scp " + kmls_path + " lg@" + GALAXY_IP +
        ":" + server_path)
    # os.system(
    #     "sshpass -p 'lqgalaxy' scp " + file_path_slave + " lg@" + GALAXY_IP +
    #     ":" + server_path)


def create_kml_file():
    files = [f for f in listdir(persistent_path) if
             isfile(join(persistent_path, f))]
    updates = [u for u in listdir(updates_path) if
               isfile(join(updates_path, u))]
    kml_file = open(kmls_path, 'w')
    for kml in files:
        kml_file.write(kmls_url + kml + "\n")
    for kml in updates:
        kml_file.write(kmls_url_upd + kml + "\n")
    kml_file.close()
    # sync_kmls_slave_file()


def send_kmls():
    create_kml_file()
    sync_kmls_to_galaxy()
