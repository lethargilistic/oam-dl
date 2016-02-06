#!/usr/bin/env python3

r'''
Download all Ozy and Millie comics.

Usage:
  oam-dl --create
  oam-dl --download-all
  oam-dl --download-num=<NUMBER>
  oam-dl --version
  oam-dl -h | --help
Options:
  --create  Creates the db of Ozy and Millie comics
  -h --help  Show help
  --version  Show version
'''
from docopt import docopt
import json
import os
import re
import requests
from os.path import expanduser
from progress.bar import Bar
__version__ = '0.1.1'
__author__ = "Mike Overby"

arguments = docopt(__doc__, version=__version__)

HOME = expanduser("~")
BASE_URL = 'http://ozyandmillie.org/comics/'
OAM_DICT_FILENAME = os.path.join(HOME, 'oam_dict.json')
ROOT_DIR = os.path.join(HOME, 'OAM')

#Create the json object representing the comic's archive
def create():
    archive = requests.get(BASE_URL)
    if archive.status_code == 200:
        archive_html = archive.text
        links = re.findall(r'<a href="(.+?)"', archive_html)
        links = links[1:] #Cut off the parent directory link in webpage
        OAM_DICT = {}
        for oam_num in range(len(links)):
            comic_info = {}

            #Save the date
            day = re.match(r'^(\d+)-(\d+)-(\d+)', links[oam_num])
            comic_info['date'] = {}
            
            comic_info['date']['year'] = int(day.group(1))
            comic_info['date']['month'] = int(day.group(2))
            comic_info['date']['day'] = int(day.group(3))

            #Save the link
            comic_info['link'] = links[oam_num]
            
            OAM_DICT[oam_num] = comic_info
        with open(OAM_DICT_FILENAME, 'w') as f:
            json.dump(OAM_DICT, f)
            print("Updated the links")
    else:
        print("The internet connection didn't work.")

#Read in the json object representing the archive
def read_in_OAM_DICT():
    if not os.path.exists(OAM_DICT_FILENAME):
        print("There is no data. Run --create")
        return None
    else:
        f = open(OAM_DICT_FILENAME, "r")
        data = json.loads(f.readline())
        f.close()
        return data

#Download a single comic
def download_one(OAM_DICT, comic):
    comic = str(comic)
    
    if not os.path.exists(ROOT_DIR):
        os.makedirs(ROOT_DIR)

    year_dir = os.path.join(ROOT_DIR, str(OAM_DICT[comic]['date']['year']))
    if not os.path.exists(year_dir):
        os.makedirs(year_dir)

    month_dir = os.path.join(year_dir, str(OAM_DICT[comic]['date']['month']))
    if not os.path.exists(month_dir):
        os.makedirs(month_dir)

    comic_path = os.path.join(month_dir, str(OAM_DICT[comic]['link']))
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

#Download a range of comics
def download_range(OAM_DICT, start, end):
    start = int(start)
    end = int(end)
    
    bar = Bar('Downloading', max=end-start+1, suffix='%(percent)d%%')
    for comic in range(start-1, end):
        try:
            download_one(OAM_DICT, comic)
        except ConnectionError:
            bar.finish()
            break
        bar.next()
    bar.finish()

#Download every comic
def download_all():
    OAM_DICT = read_in_OAM_DICT()
    if OAM_DICT is None:
        return
    download_range(OAM_DICT, 1, len(OAM_DICT))

#Download a specific comic by release number
def download_release_num():
    OAM_DICT = read_in_OAM_DICT()
    if OAM_DICT is None:
        return
    
    num = int(arguments["--download-num"])
    if num > 0 and num < len(OAM_DICT):
        try:
            download_one(OAM_DICT, num)
            print("Downloaded", num)
        except ConnectionError:
            pass
    else:
        print("Ozy and Millie is numbered 1 to", len(OAM_DICT) - 1)

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
