r'''
Download all Ozy and Millie comics.

Usage:
  oam-dl.py --update
  oam-dl.py --download-all
  oam-dl.py --download-num=<NUMBER>
  oam-dl.py --download-year=<YEAR>
  oam-dl.py --download-month=<MONTH> <YEAR>
  oam-dl.py --download-day=<DAY> <MONTH> <YEAR>
  oam-dl.py --version
  oam-dl.py -h | --help
Options:
  --create  Creates the db of Ozy and Millie comics
  -h --help  Show help
  --version  Show version
'''
from docopt import docopt
import re
import requests
import json
import os

__version__ = '0.0.1'

#arguments = docopt(__doc__, version=__version__)

BASE_URL = 'http://ozyandmillie.org/comics/'
OAM_DICT = {} #MAy be better to use a list so that each comic can be looped through in order.
OAM_DICT_FILENAME = 'oam_dict.json'
ROOT_DIR = 'OAM'
DIR = os.path.dirname(os.path.abspath(__file__)) #This file's directory

#Download all Ozy and Millie comics of all time
#Download all O&M in year
#Download all O&M in month of year
#Download O&M on a certain day
#Download O&M based on release number

def create():
    archive = requests.get(BASE_URL)
    if archive.status_code == 200:
        archive_html = archive.text
        links = re.findall(r'<a href="(.+?)"', archive_html)
        links = links[1:] #Cut off the parent directory link
        for oam_num in range(len(links)):
            comic_info = {}
            
            date = re.match(r'^(\d+)-(\d+)-(\d+)', links[oam_num])
            comic_info['date'] = {}
            comic_info['date']['year'] = date.group(1)
            comic_info['date']['month'] = date.group(2)
            comic_info['date']['day'] = date.group(3)

            comic_info['link'] = links[oam_num]
            
            OAM_DICT[oam_num] = comic_info
        with open(OAM_DICT_FILENAME, 'w') as f:
            f.write(json.dumps(OAM_DICT))
            print("Updated the links")
    else:
        print("The internet connection didn't work.")

def download_all():
    if not os.path.exists(OAM_DICT_FILENAME):
        print("Dictionary not created. run --create")
    else:
        with open(OAM_DICT_FILENAME, 'r') as f:
            OAM_DICT = json.loads(f.readline())

        if not os.path.exists(ROOT_DIR):
            os.makedirs(ROOT_DIR)
        os.chdir(ROOT_DIR)

        dl_count = 1
        for comic in OAM_DICT:
            if not os.path.exists(OAM_DICT[comic]['date']['year']):
                os.makedirs(OAM_DICT[comic]['date']['year'])

            month_dir = OAM_DICT[comic]['date']['year'] + '\\' + OAM_DICT[comic]['date']['month']
            if not os.path.exists(month_dir):
                os.makedirs(month_dir)

            comic_path = month_dir + "\\" + OAM_DICT[comic]['link']
            #print(comic_path)
            if not os.path.exists(comic_path):
                with open(comic_path, 'wb') as c:
                    link = BASE_URL + OAM_DICT[comic]['link']
                    pic = requests.get(link)
                    if pic.status_code == 200:
                        c.write(pic.content)
                    else:
                        print("[Status: " + str(pic.status_code) + "] Something interrupted the download.")
                        break
            
            print("Download in progress:", str(dl_count * 100 // len(OAM_DICT)) + "%")
            dl_count += 1
            
def download_year(year):
    pass

def download_month(month, year):
    pass

def download_day(day, month, year):
    pass

def download_release_num(num):
    pass

#fill_links()
create()
download_all()
