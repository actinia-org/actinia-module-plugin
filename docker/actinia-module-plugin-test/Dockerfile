FROM mundialis/actinia:latest as actinia_test

LABEL authors="Carmen Tawalika,Anika Weinmann"
LABEL maintainer="tawalika@mundialis.de,weinmann@mundialis.de"

ENV ACTINIA_CUSTOM_TEST_CFG /etc/default/actinia-module-plugin-test

# TODO do not set DEFAULT_CONFIG_PATH if this is fixed
ENV DEFAULT_CONFIG_PATH /etc/default/actinia-module-plugin-test
# set TEMPLATE_VALUE_ for testing
ENV TEMPLATE_VALUE_ENV_RASTER elevation
ENV TEMPLATE_VALUE_ENV_TYPE raster

# install things only for tests
RUN apk add --no-cache redis
RUN pip install --upgrade setuptools && pip install pytest pytest-cov pwgen

ENTRYPOINT ["/bin/sh"]
CMD ["/src/start.sh"]

RUN pip uninstall actinia-module-plugin.wsgi actinia-module-plugin -y

# add data for tests
RUN grass -e -c 'EPSG:3358' /actinia_core/grassdb/nc_spm_08
# RUN wget --quiet https://grass.osgeo.org/sampledata/north_carolina/nc_spm_08_micro.zip && \
#   unzip nc_spm_08_micro.zip && \
#   rm -f nc_spm_08_micro.zip && \
#   mv nc_spm_08_micro /actinia_core/grassdb/nc_spm_08
# RUN grass -e -c 'EPSG:4326' /actinia_core/grassdb/latlong_wgs84

WORKDIR /src/actinia-module-plugin/

# copy needed files and configs for test
COPY docker/actinia-module-plugin-test/actinia-module-plugin-test.cfg /etc/default/actinia
COPY docker/actinia-module-plugin-test/actinia-module-plugin-test.cfg /etc/default/actinia-module-plugin-test
COPY . /src/actinia-module-plugin/

RUN chmod a+x tests_with_redis.sh
RUN pip install .

RUN ./tests_with_redis.sh
