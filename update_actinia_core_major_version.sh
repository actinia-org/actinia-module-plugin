#!/usr/bin/env bash

############################################################################
#
# MODULE:       update_actinia_core_major_version.sh
# AUTHOR(S):    Anika Weinmann
#
# PURPOSE:      This script updates the major actinia-core version in url
#
# COPYRIGHT:    (C) 2022 by mundialis GmbH & Co. KG
#
#               This program is free software under the GNU General Public
#               License (>=v3). Read the file COPYING that comes with GRASS
#               for details.
#
#############################################################################

# execution for example with.
#     bash update_actinia_core_major_version.sh v2 v3

OLD_VERSION=$1
NEW_VERSION=$2

sed -i "s+/api/${OLD_VERSION}/+/api/${NEW_VERSION}/+g" actinia_module_plugin/static/index.html
sed -i "s+/api/${OLD_VERSION}/+/api/${NEW_VERSION}/+g" actinia-module.md
sed -i "s+ACTINIA_VERSION=\"${OLD_VERSION}\"+ACTINIA_VERSION=\"${NEW_VERSION}\"+g" docker/README.md
