#!/bin/env sh

# Install PyCSW

CSWDIR=/var/www/
mkdir -p $CSWDIR && cd $CSWDIR
git clone https://github.com/geopython/pycsw.git
cd $CSWDIR/pycsw && pip install -e . && pip install -r requirements.txt
cp -a /tmp/default.cfg $CSWDIR/pycsw
rm -R /tmp/default.cfg
exit
