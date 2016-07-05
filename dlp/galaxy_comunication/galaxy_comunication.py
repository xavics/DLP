import os
from os import listdir
from os.path import isfile, join

from dlp.apps import get_site_url, get_galaxy_ip

persistent_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")) + "/static/kmls/persistent/"
kmls_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")) + "/static/kmls/kmls.txt"
kmls_url = get_site_url() + "static/kmls/persistent/"
GALAXY_IP = get_galaxy_ip()


def sync_kmls_to_galaxy():
    server_path = "/var/www/html"
    print "sshpass -p 'lqgalaxy' scp " + kmls_path + " lg@" + GALAXY_IP + ":" + server_path
    os.system(
        "sshpass -p 'lqgalaxy' scp " + kmls_path + " lg@" + GALAXY_IP +
        ":" + server_path)
    # os.system(
    #     "sshpass -p 'lqgalaxy' scp " + file_path_slave + " lg@" + GALAXY_IP +
    #     ":" + server_path)


def create_kml_file():
    files = [f for f in listdir(persistent_path) if
             isfile(join(persistent_path, f))]
    kml_file = open(kmls_path, 'w')
    for kml in files:
        kml_file.write(kmls_url + kml + "\n")
    kml_file.close()
    # sync_kmls_slave_file()


def send_kmls():
    create_kml_file()
    sync_kmls_to_galaxy()
