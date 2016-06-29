import os
from dlp.models import *
from DLP.settings import SITE_URL

templates_path = os.path.dirname(__file__) + "/templates/"
kmls_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")) + "/static/kmls/"
kmls_url = SITE_URL + "static/kmls/"


def create_kml(template_name, kml_name, variables):
    base = open(templates_path + template_name, "r")
    string_file = base.read()
    kml = string_file.format(**variables)
    print kml
    base.close()
    temp = open(os.path.join(kmls_path, kml_name), "w")
    temp.write(kml)
    temp.close()


def fill_template(template_name, variables):
    base = open(templates_path + template_name, "r")
    string_file = base.read()
    final_html = string_file.format(**variables)
    base.close()
    print final_html
    return final_html


def create_list_test(model):
    if model == "Transport":
        create_kml("document.txt", "transports_list.kml",
                   create_items_networklink(
                       Transport.objects.filter(is_active=1)))
    elif model == "LogisticCenter":
        create_kml("document.txt", model + ".kml",
                   create_items_placemark(LogisticCenter.objects.all()))
    elif model == "DropPoint":
        create_kml("document.txt", model + ".kml",
                   create_items_placemark(DropPoint.objects.all()))
    elif model == "Layout":
        create_kml("document.txt", model + ".kml",
                   create_items_layouts(Layouts.objects.all()))
    elif model == "Packet":
        create_kml("document.txt", model + ".kml",
                   create_items_placemark(Package.objects.filter(status=1)))
    else:
        print "Bad model: {}".format(model)


def placemark_variables(item):
    return {'name': item.name,
            'description': "Placemark" + item.name,
            'style_id': "style" + item.id,
            'lat': item.lat, 'lng': item.lng, 'alt': item.lat}


def style_variables(item):
    return {'id': "style" + item.id,
            'icon': SITE_URL + item.style_url.earth_url,
            'scale': 1}


def networklink_variables(item):
    return {'name': "Transport" + str(item.id),
            'href': kmls_url + item.__class__.__name__ + str(item.id),
            'refreshInterval': 1}


def layout_variables(item):
    variables = item.__dict__
    variables['url'] = SITE_URL + variables.get('url')
    return variables


def create_items_placemark(items):
    items_str = ""
    for item in items:
        items_str += fill_template("style.kml", style_variables(item)) + "\n"
        items_str += fill_template("placemark.kml",
                                   placemark_variables(item)) + "\n"
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


'''
    The next step of that function is to make this list of city
'''


# def create_list_networklink(kml_name, model):
#     if model == "Transport":
#         link_list = Transport.objects.filter(is_active=1)
#     elif model == "LogisticCenter":
#         link_list = LogisticCenter.objects.all()
#     elif model == "DropPoint":
#         link_list = DropPoint.objects.all()
#     else:
#         link_list = None
#     with open(os.path.join(kmls_path, kml_name), "w") as kml_file:
#         kml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" +
#                        "<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n" +
#                        "\t<Document>\n")
#         for item in link_list:
#             kml_file.write("\t\t<NetworkLink>\n" +
#                            "\t\t\t<Name>" + model + " " + str(item.id) +
#                            "</Name>\n" +
#                            "\t\t\t<Link>\n" +
#                            "\t\t\t\t<href>" + kmls_url + model +
#                            str(item.id) + ".kml</href>\n" +
#                            "\t\t\t\t<refreshMode>onInterval</refreshMode>\n" +
#                            "\t\t\t\t<refreshInterval>" + str(1) +
#                            "</refreshInterval>\n" +
#                            "\t\t\t</Link>\n" +
#                            "\t\t</NetworkLink>\n")
#             if type(item) is Transport:
#                 kml_file.write("\t\t<NetworkLink>\n" +
#                                "\t\t\t<Name> Package " +
#                                str(item.package_id) + "</Name>\n" +
#                                "\t\t<Link>\n" +
#                                "\t\t<href>" + kmls_url + "package_" +
#                                str(item.package_id) + ".kml</href>\n" +
#                                "\t\t</Link>\n" +
#                                "\t\t</NetworkLink>\n")
#         kml_file.write("\t</Document>\n" +
#                        "</kml>")

# def create_layouts():
