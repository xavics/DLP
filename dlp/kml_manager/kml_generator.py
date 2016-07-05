import os
from dlp.models import *
from dlp.apps import get_site_url
import logging
from itertools import chain
import datetime

logger = logging.getLogger(__name__)
templates_path = os.path.dirname(__file__) + "/templates/"
kmls_tmp_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")) + "/static/kmls/tmp/"
kmls_persistent_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")) + "/static/kmls/persistent/"
kmls_url = get_site_url() + "static/kmls/tmp/"
# kmls_tmp_url = get_site_url() + "static/kmls/tmp/"

# Model name variables
DROPPOINT = "DropPoint"
LOGISTICCENTER = "LogisticCenter"
LAYOUT = "Layout"
PACKAGE = "Package"
TRANSPORT = "Transport"


def create_kml(template_name, kml_name, variables, tmp=False):
    base = open(templates_path + template_name, "r")
    string_file = base.read()
    kml = string_file.format(**variables)
    base.close()
    if tmp:
        temp = open(os.path.join(kmls_tmp_path, kml_name), "w")
    else:
        temp = open(os.path.join(kmls_persistent_path, kml_name), "w")
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
                       Transport.objects.filter(is_active=1)))
    elif model == LOGISTICCENTER:
        create_kml("document.txt", model + ".kml",
                   create_items_placemark(LogisticCenter.objects.all()))
    elif model == DROPPOINT:
        create_kml("document.txt", model + ".kml",
                   create_items_placemark(DropPoint.objects.all()))
    elif model == LAYOUT:
        create_kml("document.txt", model + ".kml",
                   create_items_layouts(Layouts.objects.all()))
    elif model == PACKAGE:
        create_kml("document.txt", model + ".kml",
                   create_items_placemark(chain(
                       Package.objects.filter(status=1),
                       Package.objects.filter(status=0).exclude(
                           date_delivered__lte=(
                               datetime.datetime.now() - datetime.timedelta(
                                   seconds=45))))))
    else:
        logger.error("Bad model: {}".format(model))


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


def networklink_variables(item):
    return {'name': "Transport" + str(item.id),
            'href': kmls_url + item.__class__.__name__ + str(item.id),
            'refreshInterval': 1}


def layout_variables(item):
    variables = item.__dict__
    variables['url'] = get_site_url() + variables.get('url')
    del variables['_state'], variables['id']
    return variables


def create_items_placemark(items):
    items_str = ""
    for item in items:
        items_str += str(
            fill_template("style.kml", style_variables(item))) + "\n"
        items_str += str(fill_template("placemark.kml",
                                       placemark_variables(item))) + "\n"
    return {'items': items_str}


def create_items_layouts(items):
    items_str = ""
    for item in items:
        items_str += fill_template("layout.kml", layout_variables(item)) + "\n"
    return {'items': items_str}


def create_items_networklink(items):
    items_str = ""
    for item in items:
        items_str += str(fill_template("networklink_refresh.kml",
                                       networklink_variables(item))) + "\n"
    return {'items': items_str}


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


'''
    The next step of that functions is to make this list by city if needed:
        For example when there ara a massive number of droppoints and
        Logisiticcenters items
'''
