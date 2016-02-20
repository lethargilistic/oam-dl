# Ozy and Millie Archive CLI
[![PyPI](https://img.shields.io/pypi/v/oam-dl.svg)](https://pypi.python.org/pypi/oam-dl)
[![PyPI](https://img.shields.io/pypi/l/oam-dl.svg)]()
[![PyPI](https://img.shields.io/pypi/pyversions/oam-dl.svg)]()

oam-dl is inspired by and based on xkcd-dl by Tasdik Rahman, which was inspired by youtube-dl by Daniel Bolton.

It archives the less memetic yet superior (:P) *Ozy and Millie* by Dana Simpson, which ran from 1998 to 2008.

# Features
* Download all *Ozy and Millie* comics.
* Download individual *Ozy and Millie* comics by release number.
* Download ranges of *Ozy and Millie* comics by release number.

# Installation
It's on PyPI: `pip3 install oam-dl`

# Usage
After installing, run `oam-dl --create`.
This creates a json file in your home directory that stores
information on each of the comics.

##`--download`
Downloading a comic will create a directory structure in your
home directory under OAM to automatically organize your comics 
by year and month.

### `<NUM>`
`oam-dl --download <NUM>` retrieves the `Ozy and Millie` comic with release
number <NUM>.

###`-a`
`oam-dl --download -a` retrieves every *Ozy and Millie* comic. There are >2000 of them, so the download may take a while.

###`-r`
`oam-dl --download -r <START> <END>` retieves the range of comics between
release numbers <START> and <END>.

# TODO
* Download via release date (maybe)

# License
MIT License (see LICENCE.txt)
