# Ozy and Millie Archive CLI
oam-dl is inspired by and based on xkcd-dl by Tasdik Rahman, which was inspired by youtube-dl by Daniel Bolton.

It archives the less memetic yet superior (:P) *Ozy and Millie* by Dana Simpson, which ran from 1998 to 2008.

# Features
* Download all *Ozy and Millie* comics.
* Download individual *Ozy and Millie* comics by release number.
* Download ranges of *Ozy and Millie* comics by release number.

# Usage
After installing, run `oam-dl --create`.

##`--download`
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
