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
  --update  Updates the information on Ozy and Millie comics
  -h --help  Show help
  --version  Show version
'''
from docopt import docopt
import re
import requests
import json
import os

__version__ = '0.0.1'

arguments = docopt(__doc__, version=__version__)

BASE_URL = 'http://ozyandmillie.org'
ARCHIVE_URL = 'http://ozyandmillie.org/comics/'
OAM_DICT = {}
OAM_DICT_FILENAME = 'oam_dict.json'

#Download all Ozy and Millie comics of all time
#Download all O&M in year
#Download all O&M in month of year
#Download O&M on a certain day
#Download O&M based on release number

def fill_links():
    archive = requests.get(ARCHIVE_URL)
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

def update_links():
    pass

def download_all():
    pass

def download_year(year):
    pass

def download_month(month, year):
    pass

def download_day(day, month, year):
    pass

def download_release_num(num):
    pass

fill_links()
