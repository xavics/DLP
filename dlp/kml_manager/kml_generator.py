import os
import logging
from itertools import chain
import datetime
import time

from DLP.settings import STATIC_ROOT
from dlp.models import *
from dlp.apps import get_site_url

logger = logging.getLogger(__name__)

# Paths
TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), "templates/")
KMLS_PATH = os.path.join(STATIC_ROOT, "kmls/")
KMLS_TMP_PATH = os.path.join(STATIC_ROOT, "kmls/tmp/")
KMLS_PERSISTENT_PATH = os.path.join(STATIC_ROOT, "kmls/persistent/")
KMLS_UPDATES_PATH = os.path.join(STATIC_ROOT, "kmls/updates/")
KMLS_DELIVERS_PATH = os.path.join(STATIC_ROOT, "kmls/delivers/")
KMLS_TMP_URL = "{site_url}{r_path}".format(
    site_url=get_site_url(), r_path="static/kmls/tmp/")
KMLS_DELIVERS_URL = "{site_url}{r_path}".format(
    site_url=get_site_url(), r_path="static/kmls/delivers/")
KMLS_UPDATE_URL = "{site_url}{r_path}".format(
    site_url=get_site_url(), r_path="static/kmls/persistent/")

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
    base = open(os.path.join(TEMPLATES_PATH, template_name), "r")
    string_file = base.read()
    kml = string_file.format(**variables)
    base.close()
    if directory == TMP:
        temp = open(os.path.join(KMLS_TMP_PATH, kml_name), "w")
    elif directory == PERSISTENT:
        temp = open(os.path.join(KMLS_PERSISTENT_PATH, kml_name), "w")
    elif directory == UPDATES:
        temp = open(os.path.join(KMLS_UPDATES_PATH, kml_name), "w")
    else:
        temp = open(os.path.join(KMLS_DELIVERS_PATH, kml_name), "w")
    temp.write(kml)
    temp.close()


def fill_template(template_name, variables):
    base = open(os.path.join(TEMPLATES_PATH, template_name), "r")
    string_file = base.read()
    format_template = string_file.format(**variables)
    base.close()
    return str(format_template)


def create_list_test(model):
    if model == TRANSPORT:
        create_kml("document.txt", get_document_name(model),
                   create_items_networklink(
                       Transport.objects.filter(
                           status=Transport.TransportStatus.ACTIVE
                       ), model),
                   DELIVERS)
    elif model == LOGISTICCENTER:
        create_kml("document.txt", get_document_name(model),
                   create_items_placemark(LogisticCenter.objects.all(), model),
                   PERSISTENT)
    elif model == DROPPOINT:
        create_kml("document.txt", get_document_name(model),
                   create_items_placemark(DropPoint.objects.all(), model),
                   PERSISTENT)
    elif model == LAYOUT:
        create_kml("document.txt", get_document_name(model),
                   create_items_layouts(Layouts.objects.all(), model),
                   PERSISTENT)
    elif model == PACKAGE:
        create_kml("document.txt", get_document_name(model),
                   create_items_placemark(chain(
                       Package.objects.filter(
                           status=Package.PackageStatus.SENDING),
                       Package.objects.filter(
                           status=Package.PackageStatus.SENT).exclude(
                           date_delivered__lte=(
                               datetime.datetime.now() - datetime.timedelta(
                                   seconds=45)))), model), DELIVERS)
    else:
        logger.error("Bad model: {}".format(model))


def get_document_name(model):
    return "{model}.kml".format(model=model)


def create_updates(model):
    if model == LOGISTICCENTER:
        variables = create_items_placemark(LogisticCenter.objects.all(), model)
        variables['targetHref'] = "{url}{modal}.kml".format(
            url=KMLS_UPDATE_URL, model=model)
    else:
        variables = create_items_placemark(DropPoint.objects.all(), model)
        variables['targetHref'] = "{url}{modal}.kml".format(
            url=KMLS_UPDATE_URL, model=model)
    name = "update_{model}_{time}.kml".format(
        model=model, time=int(time.mktime(datetime.datetime.now().timetuple()))
    )
    create_kml("update_document.txt", name, variables, UPDATES)


def create_delivers():
    delivers = [u for u in os.listdir(KMLS_DELIVERS_PATH) if
                os.path.isfile(os.path.join(KMLS_DELIVERS_PATH, u))]
    variables = create_items_networklink(delivers, DELIVERS, True)
    create_kml("document.txt", "delivers.kml", variables, PERSISTENT)


def placemark_variables(item):
    if item.__class__.__name__ == PACKAGE:
        item.lat = item.drop_point.lat
        item.lng = item.drop_point.lng
        item.alt = item.drop_point.alt
    return {'name': item.name,
            'description': "Placemark {model}{id}".format(
                model=item.__class__.__name__, id=item.id),
            'id_style': "style_{model}{id}".format(
                model=item.__class__.__name__, id=item.id),
            'lat': item.lat, 'lng': item.lng, 'alt': item.alt}


def style_variables(item):
    return {
        'id': "style_{model}{id}".format(
            model=item.__class__.__name__, id=item.id),
        'icon': "{site_url}{st_url}".format(
            site_url=get_site_url(), st_url=item.style_url.earth_url),
        'scale': 1}


def networklink_variables(item, deliver=False):
    if deliver:
        return {'name': item,
                'href': "{url}{item}".format(url=KMLS_DELIVERS_URL, item=item)}
    else:
        return {'name': "Transport {id}".format(id=item.id),
                'href': "{url}{model}{id}.kml".format(
                    url=KMLS_TMP_URL, model=item.__class__.__name__, id=item.id
                ),
                'refreshInterval': 1}


def layout_variables(item):
    variables = item.__dict__
    variables['url'] = "{site_url}{url}".format(
        site_url=get_site_url(), url=variables.get('url'))
    del variables['_state'], variables['id']
    return variables


def create_items_placemark(items, model):
    items_str = ""
    for item in items:
        items_str.join("{var}\n".format(
            var=fill_template("style.kml", style_variables(item))))
        items_str.join("{var}\n".format(
            var=fill_template("placemark.kml", placemark_variables(item))))
    return {'id': model, 'items': items_str}


def create_items_layouts(items, model):
    items_str = ""
    for item in items:
        items_str.join("{var}\n".format(
            var=fill_template("layout.kml", layout_variables(item))))
    return {'id': model, 'items': items_str}


def create_items_networklink(items, model, deliver=False):
    template = "networklink_simple.kml" if deliver \
        else "networklink_refresh.kml"
    items_str = ""
    for item in items:
        items_str.join("{var}\n".format(
            var=str(fill_template(template, networklink_variables(item,
                                                                  deliver)))))
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


def remove_update(name):
    # os.system("find {path} -type f -name '*{name}*' -delete".format(
    #     path=KMLS_UPDATES_PATH, name=name))
    print("find {path} -type f -name '*{name}*' -delete".format(
        path=KMLS_UPDATES_PATH, name=name))


def remove_all_updates():
    print("rm -r {path}*".format(path=KMLS_UPDATES_PATH))


def remove_kml_folders():
    os.system("rm -r {path}".format(path=KMLS_PATH))


def create_kml_folders():
    os.system("mkdir {path}".format(path=KMLS_PATH))
    os.system("mkdir {path}".format(path=KMLS_TMP_PATH))
    os.system("mkdir {path}".format(path=KMLS_PERSISTENT_PATH))
    os.system("mkdir {path}".format(path=KMLS_UPDATES_PATH))
    os.system("mkdir {path}".format(path=KMLS_DELIVERS_PATH))


'''
    The next step of that functions is to make this list by city if needed:
        For example when there ara a massive number of droppoints and
        Logisiticcenters items
'''
