#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SPDX-FileCopyrightText: (c) 2018-2026 by mundialis GmbH & Co. KG

SPDX-License-Identifier: Apache-2.0

Documentation objects for GRASS modules and actinia modules api endpoints
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-2026 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


import copy

from actinia_module_plugin.model.responseModels import (
    SimpleStatusCodeResponseModel,
)

from actinia_module_plugin.model.modules import Module, ModuleList


null = "null"


listModules_get_docs = {
    "tags": ["Module Viewer"],
    "description": "Get a list of modules. "
    "Minimum required user role: user.",
    "parameters": [
        {
            "in": "path",
            "name": "tag",
            "type": "string",
            "description": "Filter for categories",
        },
        {
            "in": "path",
            "name": "category",
            "type": "string",
            "description": "Another filter for categories",
        },
        {
            "in": "path",
            "name": "family",
            "type": "string",
            "description": "Type of GRASS GIS module",
            "enum": [
                "d",
                "db",
                "g",
                "i",
                "m",
                "ps",
                "r",
                "r3",
                "t",
                "test",
                "v",
            ],
        },
        {
            "in": "path",
            "name": "record",
            "type": "string",
            "description": "If set to 'full', all information about the "
            "returned modules are given like in the single "
            "module description. Depending on active cache, "
            "this response might run into a timeout. A filter "
            "can prevent this.",
        },
    ],
    "responses": {
        "200": {
            "description": "This response returns a list of module names and "
            "the status.",
            "schema": ModuleList,
            "show persistent results might be added within future. Without this parameter "
            "no outputs are returned. No effect for single GRASS GIS modules.",
            "enum": [
                "export",
                # "persistent",
            ],
        },
    ],
    "description": "Get the description of a module. "
    "Minimum required user role: user."
    "Can be also used to reload cache for a certain module"
    "for the full module description in listModules.",
    "responses": {
        "200": {
            "description": "This response returns a description of a module.",
            "schema": Module,
        },
        "400": {
            "description": "The error message and a detailed log why "
            "describing modules did not succeeded",
            "schema": SimpleStatusCodeResponseModel,
        },
        "404": {
            "description": "The error message that the module was not found.",
            "schema": SimpleStatusCodeResponseModel,
        },
    },
}


describeActiniaModule_get_docs = copy.deepcopy(describeModule_get_docs)
describeActiniaModule_get_docs["parameters"][0]["name"] = "actiniamodule"

describeGrassModule_get_docs = copy.deepcopy(describeModule_get_docs)
describeGrassModule_get_docs["parameters"][0]["name"] = "grassmodule"
