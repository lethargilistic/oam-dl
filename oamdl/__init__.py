#!/usr/bin/env python3

r'''
Download all Ozy and Millie comics.

Usage:
  oam-dl --create
  oam-dl --download (<NUM> | -r <START> <END> | -a) 
  oam-dl -h | --help
  oam-dl --version

Options:
       --create    Creates the db of Ozy and Millie comics
       --download  Download the comic...
         <NUM>       with this release number
         -r          with release numbers from <START> to <END>
         -a          in its entirety  (may take a while)
  -h, --help       Show help
      --version    Show version
'''

from docopt import docopt
from os.path import expanduser
from progress.bar import Bar
import json
import os
import re
import requests

__version__ = '0.2.0'
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
    with open(OAM_DICT_FILENAME, "r") as f:
        data = json.loads(f.readline())
        return data

def is_valid_release_num(OAM_DICT, num):
    return 0 < num < len(OAM_DICT)

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
            print("There was a connection error. Download halted.")
            break
        bar.next()
    bar.finish()

def int_value_error_msg():
    print("The release numbers must be integers.")

#Command for downloading every comic
def download_all():
    OAM_DICT = read_in_OAM_DICT()
    if OAM_DICT:
       download_range(OAM_DICT, 1, len(OAM_DICT))

#Command for downloading a specific comic by release number
def download_release_num():
    OAM_DICT = read_in_OAM_DICT()
    try:
        num = int(arguments["<NUM>"])
    except ValueError:
        int_value_error_msg()
        return 

    if OAM_DICT and is_valid_release_num(OAM_DICT, num):
        download_one(OAM_DICT, num)
        print("Downloaded", num)

# Command for downloading a range of comics by release number
def download_release_num_range():
    OAM_DICT = read_in_OAM_DICT()
    if OAM_DICT is None:
        return
    
    try:
        start = int(arguments["<START>"])
        end = int(arguments["<END>"])
    except ValueError:
        int_value_error_msg()
        return 

    if start > end:
        print("Start must be lower than N")
        return 

    if is_valid_release_num(OAM_DICT, start) and is_valid_release_num(OAM_DICT, end):
        try:
            download_range(OAM_DICT, start, end)
            print("Downloaded from", start, "to", end)
        except ConnectionError:
            pass

def find_date(date_str):
    pass
    '''dateregex = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
    if not dateregex.match(date_str)
        print("That date did not match yyyy-mm-dd")
        return
    matches = re.find("")'''

def main():
    if arguments["--create"]:
        create()
    elif arguments["--download"]:
        if arguments["<NUM>"]:
            download_release_num()
        elif arguments["<START>"] or arguments["<END>"]:
            download_release_num_range()
        elif arguments["-a"]:
            download_all()
    elif arguments["-h"] or arguments["--help"]:
        print(__doc__)
    else:
        print("oam-dl: invalid option")
        print("Try 'oam-dl --help' for more information")

if __name__ == '__main__':
    main()
