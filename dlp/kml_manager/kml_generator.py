import os
from os import listdir
from os.path import isfile, join

import logging
from itertools import chain
import datetime
import time

from dlp.models import *
from dlp.apps import get_site_url


logger = logging.getLogger(__name__)

# Paths
templates_path = os.path.dirname(__file__) + "/templates/"
kmls_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")) + "/static/kmls/"
kmls_tmp_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")) + "/static/kmls/tmp/"
kmls_persistent_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")) + "/static/kmls/persistent/"
kmls_updates_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")) + "/static/kmls/updates/"
kmls_delivers_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")) + "/static/kmls/delivers/"
kmls_tmp_url = get_site_url() + "static/kmls/tmp/"
kmls_delivers_url = get_site_url() + "static/kmls/delivers/"
kmls_update_url = get_site_url() + "static/kmls/persistent/"

# Model name variables
DROPPOINT = "DropPoint"
LOGISTICCENTER = "LogisticCenter"
LAYOUT = "Layout"
PACKAGE = "Package"
TRANSPORT = "Transport"

# Folder KML
PERSISTENT = "persistent"
TMP = "tmp"
UPDATES = "updates"
DELIVERS = "delivers"


def create_kml(template_name, kml_name, variables, directory):
    base = open(templates_path + template_name, "r")
    string_file = base.read()
    kml = string_file.format(**variables)
    base.close()
    if directory == TMP:
        temp = open(os.path.join(kmls_tmp_path, kml_name), "w")
    elif directory == PERSISTENT:
        temp = open(os.path.join(kmls_persistent_path, kml_name), "w")
    elif directory == UPDATES:
        temp = open(os.path.join(kmls_updates_path, kml_name), "w")
    else:
        temp = open(os.path.join(kmls_delivers_path, kml_name), "w")
    temp.write(kml)
    temp.close()


def fill_template(template_name, variables):
    base = open(templates_path + template_name, "r")
    string_file = base.read()
    format_template = string_file.format(**variables)
    base.close()
    return str(format_template)


def create_list_test(model):
    if model == TRANSPORT:
        create_kml("document.txt", model + ".kml",
                   create_items_networklink(
                       Transport.objects.filter(is_active=1), model),
                   DELIVERS)
    elif model == LOGISTICCENTER:
        create_kml("document.txt", model + ".kml",
                   create_items_placemark(LogisticCenter.objects.all(), model),
                   PERSISTENT)
    elif model == DROPPOINT:
        create_kml("document.txt", model + ".kml",
                   create_items_placemark(DropPoint.objects.all(), model),
                   PERSISTENT)
    elif model == LAYOUT:
        create_kml("document.txt", model + ".kml",
                   create_items_layouts(Layouts.objects.all(), model),
                   PERSISTENT)
    elif model == PACKAGE:
        create_kml("document.txt", model + ".kml",
                   create_items_placemark(chain(
                       Package.objects.filter(status=1),
                       Package.objects.filter(status=0).exclude(
                           date_delivered__lte=(
                               datetime.datetime.now() - datetime.timedelta(
                                   seconds=45)))), model), DELIVERS)
    else:
        logger.error("Bad model: {}".format(model))


def create_updates(model):
    if model == LOGISTICCENTER:
        variables = create_items_placemark(LogisticCenter.objects.all(), model)
        variables['targetHref'] = kmls_update_url + model + ".kml"
    else:
        variables = create_items_placemark(DropPoint.objects.all(), model)
        variables['targetHref'] = kmls_update_url + model + ".kml"
    name = "update_" + model + "_" + str(
        int(time.mktime(datetime.datetime.now().timetuple()))) + ".kml"
    create_kml("update_document.txt", name, variables, UPDATES)


def create_delivers():
    delivers = [u for u in listdir(kmls_delivers_path) if
                isfile(join(kmls_delivers_path, u))]
    variables = create_items_networklink(delivers, DELIVERS, True)
    create_kml("document.txt", "delivers.kml", variables, PERSISTENT)


def placemark_variables(item):
    if item.__class__.__name__ == PACKAGE:
        item.lat = item.dropPoint.lat
        item.lng = item.dropPoint.lng
        item.alt = item.dropPoint.alt
    return {'name': item.name,
            'description': "Placemark " + item.__class__.__name__ + str(
                item.id),
            'id_style': "style_" + item.__class__.__name__ + str(item.id),
            'lat': item.lat, 'lng': item.lng, 'alt': item.alt}


def style_variables(item):
    return {'id': "style_" + item.__class__.__name__ + str(item.id),
            'icon': get_site_url() + item.style_url.earth_url,
            'scale': 1}


def networklink_variables(item, deliver=False):
    if deliver:
        return {'name': item,
                'href': kmls_delivers_url + item}
    else:
        return {'name': "Transport" + str(item.id),
                'href': kmls_tmp_url + item.__class__.__name__ +
                        str(item.id) + ".kml",
                'refreshInterval': 1}


def layout_variables(item):
    variables = item.__dict__
    variables['url'] = get_site_url() + variables.get('url')
    del variables['_state'], variables['id']
    return variables


def create_items_placemark(items, model):
    items_str = ""
    for item in items:
        items_str += str(
            fill_template("style.kml", style_variables(item))) + "\n"
        items_str += str(fill_template("placemark.kml",
                                       placemark_variables(item))) + "\n"
    return {'id': model, 'items': items_str}


def create_items_layouts(items, model):
    items_str = ""
    for item in items:
        items_str += fill_template("layout.kml", layout_variables(item)) + "\n"
    return {'id': model, 'items': items_str}


def create_items_networklink(items, model, deliver=False):
    items_str = ""
    if deliver:
        template = "networklink_simple.kml"
    else:
        template = "networklink_refresh.kml"
    for item in items:
        items_str += str(fill_template(template,
                                       networklink_variables(item,
                                                             deliver))) + "\n"
    return {'id': model, 'items': items_str}


def create_droppoints_list():
    logger.info("Creating Drop Points list")
    create_list_test(DROPPOINT)


def create_logisticcenters_list():
    logger.info("Creating Logistic Centers list")
    create_list_test(LOGISTICCENTER)


def create_layouts_list():
    logger.info("Creating Layouts list")
    create_list_test(LAYOUT)


def create_transports_list():
    logger.info("Creating Transports list")
    create_list_test(TRANSPORT)


def create_packages_list():
    logger.info("Creating Packages list")
    create_list_test(PACKAGE)


def remove_updates():
    os.system("rm -r " + kmls_updates_path + "*")


def remove_kml_folders():
    os.system("rm -r " + kmls_path + "*")


def create_kml_folders():
    os.system("mkdir " + kmls_path)
    os.system("mkdir " + kmls_tmp_path)
    os.system("mkdir " + kmls_persistent_path)
    os.system("mkdir " + kmls_updates_path)
    os.system("mkdir " + kmls_delivers_path)


'''
    The next step of that functions is to make this list by city if needed:
        For example when there ara a massive number of droppoints and
        Logisiticcenters items
'''
