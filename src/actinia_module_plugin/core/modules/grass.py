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


GRASS GIS module viewer
"""

__license__ = "Apache-2.0"
__author__ = "Anika Weinmann, Carmen Tawalika, Julia Haas"
__copyright__ = "Copyright 2019 - 2022, mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"


import json
import time

from actinia_core.models.response_models import create_response_from_model
from actinia_core.core.common.config import Configuration

from actinia_module_plugin.core.modules.processor import run_process_chain
from actinia_module_plugin.core.modules.parser import ParseInterfaceDescription
from actinia_module_plugin.model.modules import Module
from actinia_module_plugin.resources.logging import log
from actinia_module_plugin.core.modules.grass_modules_kvdb_interface import (
    kvdb_grass_module_interface,
)
from actinia_module_plugin.core.modules.accessible_modules_kvdb_interface import (
    getAccessibleModuleListKvdb,
)


def installGrassAddon(self, addon_name):
    """This function installs an official GRASS addon."""
    process_chain = {
        "version": 1,
        "list": [
            {
                "id": "1",
                "module": "g.extension",
                "inputs": [{"param": "extension", "value": addon_name}],
                "flags": "s",
            }
        ],
    }

    response = run_process_chain(self, process_chain)

    return response


def createModuleList(self):
    process_chain = {
        "version": 1,
        "list": [
            {
                "id": "g_search_modules_1",
                "module": "g.search.modules",
                "inputs": [{"param": "keyword", "value": ""}],
                "flags": "j",
            }
        ],
    }

    response = run_process_chain(self, process_chain)

    j_data = json.loads(response["process_log"][-1]["stdout"])

    # overwrite previous entries commited by EphemeralModuleLister in case the
    # further processing fails (e.g. invalid json). Else, the resource exists
    # and shows the output of g.search.modules.
    data = create_response_from_model(
        user_id=self.user_id,
        resource_id=self.resource_id,
        status="",
        orig_time=time.time(),
        orig_datetime="",
        message="",
    )
    self.resource_logger.commit(
        user_id=self.user_id,
        resource_id=self.resource_id,
        iteration=1,
        document=data,
        expiration=1,
    )

    module_list = []
    for data in j_data:
        description = data["attributes"]["description"]
        keywords = data["attributes"]["keywords"]
        name = data["name"]
        categories = keywords.split(",")
        categories.append("grass-module")
        module_response = Module(
            id=name, description=description, categories=sorted(categories)
        )
        module_list.append(module_response)

    return module_list


def createModuleUserList(self):
    return getAccessibleModuleListKvdb(self)


def build_and_run_iface_description_pc(self, module_list):
    pc = {"version": 1, "list": []}

    process_chain_items = []
    count = 1
    for module in module_list:
        if type(module) is str:
            module_id = module
        else:
            module_id = module["id"]
        process_chain_items.append(
            {
                "id": str(count),
                "module": module_id,
                "interface-description": True,
            }
        )
        count = count + 1

    pc["list"] = process_chain_items

    response = run_process_chain(self, pc)

    return response["process_log"]


def connect():
    """This method initializes the connection with kvdb."""
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

    kvdb_grass_module_interface.connect(
        host=server, port=port, password=kvdb_password
    )

    return kvdb_grass_module_interface


def cacheGrassModule(grass_module):
    """
    Insert grass_module into database
    """
    kvdb_grass_module_interface = connect()
    cached_module = kvdb_grass_module_interface.create(grass_module)

    return cached_module


def createGrassModule(self, module):
    module_list = [module]
    process_log = build_and_run_iface_description_pc(self, module_list)

    xml_string = process_log[0]["stdout"]
    grass_module = ParseInterfaceDescription(xml_string)

    # Check if cached module exists, then update if it has changed
    # This is currently the only mechanism to update a cached
    # module via API call.
    # If not, then cache it
    kvdb_grass_module_interface = connect()
    if kvdb_grass_module_interface.exists(module):
        kvdb_grass_module_interface.update(module, grass_module)
    else:
        cacheGrassModule(grass_module)

    return grass_module


def createFullModuleList(self, module_list):
    detailed_module_list = []
    request_module_list = []

    # Check if modules are already cached, then use them
    for module in module_list:
        kvdb_grass_module_interface = connect()
        grass_module = kvdb_grass_module_interface.read(module["id"])
        if grass_module:
            detailed_module_list.append(grass_module)
        else:
            request_module_list.append(module)

    # If they are not in cache, request and cache them
    if len(request_module_list) > 0:
        process_log = build_and_run_iface_description_pc(
            self, request_module_list
        )

        for desc in process_log:
            try:
                grass_module = ParseInterfaceDescription(desc["stdout"])
                cacheGrassModule(grass_module)
                detailed_module_list.append(grass_module)
            except Exception:
                log.error("error parsing module %s" % desc["executable"])

    return detailed_module_list
