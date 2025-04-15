#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2018-2021 mundialis GmbH & Co. KG

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Accessible Modules Kvdb Interface
"""

__license__ = "Apache-2.0"
__author__ = "Anika Weinmann, Carmen Tawalika, Guido Riembauer, Julia Haas"
__copyright__ = "Copyright 2021 - 2022, mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"

from actinia_core.core.kvdb_user import KvdbUserInterface
from actinia_core.core.common.config import Configuration


def getAccessibleModuleListKvdb(self):
    kvdb_interface = KvdbUserInterface()
    conf = Configuration()
    try:
        conf.read()
    except Exception:
        pass

    server = conf.KVDB_SERVER_URL
    port = conf.KVDB_SERVER_PORT
    if conf.KVDB_SERVER_PW:
        kvdb_password = conf.KVDB_SERVER_PW
    else:
        kvdb_password = None
    kvdb_interface.connect(host=server, port=port, password=kvdb_password)
    user = self.user.get_id()
    access_modules = kvdb_interface.get_credentials(user)["permissions"][
        "accessible_modules"
    ]
    kvdb_interface.disconnect()
    return access_modules


def addGrassAddonToModuleListKvdb(self, grassmodule):
    """
    This function adds installed GRASS addon to the user's module list
    in kvdb.
    """
    self.user.add_accessible_modules(
        [
            grassmodule,
        ]
    )
    self.user.update()
