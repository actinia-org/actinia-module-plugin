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


Accessible Modules Redis Interface
"""

__license__ = "Apache-2.0"
__author__ = "Anika Weinmann, Carmen Tawalika, Guido Riembauer, Julia Haas"
__copyright__ = "Copyright 2021 - 2022, mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"

from actinia_core.core.redis_user import RedisUserInterface
from actinia_core.core.common.config import Configuration


def getAccessibleModuleListRedis(self):
    redis_interface = RedisUserInterface()
    conf = Configuration()
    try:
        conf.read()
    except Exception:
        pass

    server = conf.REDIS_SERVER_URL
    port = conf.REDIS_SERVER_PORT
    if conf.REDIS_SERVER_PW:
        redis_password = conf.REDIS_SERVER_PW
    else:
        redis_password = None
    redis_interface.connect(host=server, port=port, password=redis_password)
    user = self.user.get_id()
    access_modules = redis_interface.get_credentials(user)["permissions"][
        "accessible_modules"
    ]
    redis_interface.disconnect()
    return access_modules


def addGrassAddonToModuleListRedis(self, grassmodule):
    """This function adds installed GRASS addon to the user's module list
    in redis.
    """
    self.user.add_accessible_modules(
        [
            grassmodule,
        ]
    )
    self.user.update()
