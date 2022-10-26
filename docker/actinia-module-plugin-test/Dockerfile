FROM mundialis/actinia:latest as actinia_test

LABEL authors="Carmen Tawalika,Anika Weinmann"
LABEL maintainer="tawalika@mundialis.de,weinmann@mundialis.de"

ENV ACTINIA_CUSTOM_TEST_CFG /etc/default/actinia-module-plugin-test

# TODO do not set DEFAULT_CONFIG_PATH if this is fixed
ENV DEFAULT_CONFIG_PATH /etc/default/actinia-module-plugin-test

# install things only for tests
RUN apk add redis
RUN pip3 install iniconfig colorlog pwgen

ENTRYPOINT ["/bin/sh"]
CMD ["/src/start.sh"]

RUN pip3 uninstall actinia-module-plugin.wsgi -y

# # add data for tests
# RUN wget --quiet https://grass.osgeo.org/sampledata/north_carolina/nc_spm_08_micro.zip && \
#   unzip nc_spm_08_micro.zip && \
#   rm -f nc_spm_08_micro.zip && \
#   mv nc_spm_08_micro /actinia_core/grassdb/nc_spm_08
# RUN grass -e -c 'EPSG:4326' /actinia_core/grassdb/latlong_wgs84

# copy needed files and configs for test
COPY docker/actinia-module-plugin-test/actinia-module-plugin-test.cfg /etc/default/actinia
COPY docker/actinia-module-plugin-test/actinia-module-plugin-test.cfg /etc/default/actinia-module-plugin-test
COPY . /src/actinia-module-plugin/

WORKDIR /src/actinia-module-plugin/

RUN chmod a+x tests_with_redis.sh
RUN python3 setup.py install

#RUN ./tests_with_redis.sh
