r'''
Download all Ozy and Millie comics.

Usage:
  oam-dl.py --create
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
__author__ = "Mike Overby"

arguments = docopt(__doc__, version=__version__)

BASE_URL = 'http://ozyandmillie.org/comics/'
OAM_DICT_FILENAME = 'oam_dict.json'
ROOT_DIR = 'OAM'

#Download all Ozy and Millie comics
#Download O&M based on release number

#These will run O(n) with dict, but perhaps O(log n) with a list or tree.
#Or figure out the boundary numbers in O(log n) and just index the dict normally!
    #Download from some start date to some date
        #Download all O&M in year
        #Download all O&M in month of year
        #Download O&M on a certain day

def create():
    archive = requests.get(BASE_URL)
    if archive.status_code == 200:
        archive_html = archive.text
        links = re.findall(r'<a href="(.+?)"', archive_html)
        links = links[1:] #Cut off the parent directory link
        OAM_DICT = {}
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
            json.dump(OAM_DICT, f)
            print("Updated the links")
    else:
        print("The internet connection didn't work.")

def ensure_OAM_DICT():
    if not os.path.exists(OAM_DICT_FILENAME):
        print("There is no data. Run --create")
        return None
    else:
        f = open(OAM_DICT_FILENAME, "r")
        data = json.loads(f.readline())
        f.close()
        return data
    
def download_one(OAM_DICT, comic):
    if not os.path.exists(ROOT_DIR):
        os.makedirs(ROOT_DIR)

    year_dir = ROOT_DIR + '\\' + OAM_DICT[comic]['date']['year']
    if not os.path.exists(year_dir):
        os.makedirs(year_dir)

    month_dir = year_dir + '\\' + OAM_DICT[comic]['date']['month']
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
                c.close()
                print("[Status: " + str(pic.status_code) + "] Something interrupted the download.")
                raise ConnectionError

def download_all():
    OAM_DICT = ensure_OAM_DICT()
    if OAM_DICT is None:
        return

    dl_count = 1
    for comic in OAM_DICT:
        try:
            download_one(OAM_DICT, int(comic))                
            print("Download in progress:", str(dl_count * 100 // len(OAM_DICT)) + "%")                
            dl_count += 1
        except ConnectionError:
            break

def download_release_num():
    OAM_DICT = ensure_OAM_DICT()
    if OAM_DICT is None:
        return
    
    num = int(arguments["--download-num"])
    if num > 0 and num < len(OAM_DICT):
        try:
            download_one(OAM_DICT, str(num))
            print("Downloaded", num)
        except ConnectionError:
            pass
    else:
        print("Ozy and Millie is numbered 1 to", len(OAM_DICT) - 1)

def download_year(year):
    pass

def download_month(month, year):
    pass

def download_day(day, month, year):
    pass

def main():
    if arguments["--create"]:
        create()
    elif arguments["--download-num"]:
        download_release_num()
    elif arguments["--download-all"]:
        download_all()
    elif arguments["-h"] or arguments["--help"]:
        print(__doc__)
    elif arguments["--version"]:
        print(__version__, __author__)
    else:
        print(__doc__)

if __name__ == '__main__':
    main()
