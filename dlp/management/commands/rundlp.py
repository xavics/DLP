import os
import re

from django.core.management.base import BaseCommand, CommandError

from DLP.settings import PROJECT_ROOT
from dlp.kml_manager.kml_generator import create_logisticcenters_list, \
    create_droppoints_list, create_layouts_list

PATTERN_IP = "^([m01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]" + \
             "\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\." + \
             "([01]?\\d\\d?|2[0-4]\\d|25[0-5])$"

PATTERN_IPADDR = "^([m01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?" + \
                 "|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])" + \
                 "\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5]):(\d{1,5})$"


def write_ip(ip_galaxy, site_url):
    f = open(os.path.join(PROJECT_ROOT, 'ipsettings'), 'w')
    line = ip_galaxy + "," + site_url
    print line
    f.write(line)
    f.close()


class Command(BaseCommand):
    PATH_TMP = os.path.join(PROJECT_ROOT, "dlp/static/kmls/tmp/")
    PATH_PERSISTENT = os.path.join(PROJECT_ROOT,
                                   "dlp/static/kmls/persistent/")
    help = 'Set the <ip> of the galaxy Liquid system.'


    def add_arguments(self, parser):
        parser.add_argument('ip', nargs='?',
                            help='Mandatory galaxy liquid ip address')
        parser.add_argument('addrport', nargs='?',
                            help='Optional port number, or ipaddr:port')

    def handle(self, *args, **options):
        try:
            parsed_ip = options['ip']
            pattern_ip = re.compile(PATTERN_IP)
            pattern_ipaddr = re.compile(PATTERN_IPADDR)
            if pattern_ip.match(parsed_ip) or pattern_ipaddr.match(parsed_ip):
                if not options['addrport']:
                    app_ip = "127.0.0.1:8000"
                else:
                    app_ip = options['addrport']
                site_url = "http://" + app_ip + "/"
                write_ip(parsed_ip, site_url)
                self.stdout.write(self.style.SUCCESS(
                    'Successfully changed the ip to "%s"' % parsed_ip))
                # Erasing the files and Databases with KMl and
                # other dynamic information created during the FAED run.
                self.create_system_files()
                os.system("rm -r " + self.PATH_TMP + "*")
                os.system("rm -r " + self.PATH_PERSISTENT + "*")
                # self.clear_databases()
                # Creating the KMl files with the information of the Database
                self.create_base_kml()
                os.system("bash rundlp " + app_ip)
            else:
                self.stdout.write(
                    self.style.error(
                        'Ip "%s" have an incorrect format' % parsed_ip))
        except:
            raise CommandError('FAED cannot be raised')

    # def clear_databases(self):
    #     self.stdout.write("Deleting data from Kml and Incidences ...")
    #     try:
    #         Kml.objects.all().delete()
    #         Incidence.objects.all().delete()
    #         sync_kmls_file()
    #         sync_kmls_to_galaxy()
    #     except Exception:
    #         self.stdout.write(self.style.error("Error deleting data from" +
    #                                            " the tables."))

    def create_system_files(self):
        self.stdout.write("Creating startUp files...")
        os.system("mkdir -p " + self.PATH_TMP)
        os.system("mkdir -p " + self.PATH_PERSISTENT)

    def create_base_kml(self):
        create_logisticcenters_list()
        create_droppoints_list()
        create_layouts_list()
        # self.stdout.write("Creating Weather Kml...")
        # generate_weather(BASE_DIR + "/faed_management/static/kml/")
        self.stdout.write("KMLs files done")
