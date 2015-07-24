FROM datacats/web

MAINTAINER boxkite

RUN apt-get update -y

RUN apt-get install -y gdal-bin

RUN mkdir -p /source && git clone -q https://github.com/deniszgonjanin/geopusher /source

RUN pip install -r /source/requirements.txt

ADD ./entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD python /source/geopusher/main.py
