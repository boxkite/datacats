##
# Based on geographica/pycsw:2.0-dev
# Author Cayetano Benavent <cayetano.benavent@geographica.gs>
# 
# This image runs a pycsw server on an internal port 8000.
#

FROM datacats/web

MAINTAINER boxkite

# Based on https://github.com/GeographicaGS/Docker-PyCSW/

RUN DEBIAN_FRONTEND=noninteractive apt-get -q -y install \
    software-properties-common \
    python-software-properties \
    python-sqlalchemy \
    sqlite3 \
    libproj-dev \
    git \
    python-pip \
    zlib1g-dev \
    libgeos-dev \
    libgeos++-dev

# install PyCSW
ADD ./default.cfg /tmp/
ADD ./install_pycsw.sh /tmp/
RUN sh /tmp/install_pycsw.sh

EXPOSE 8000

# Output version
CMD pip show pycsw
