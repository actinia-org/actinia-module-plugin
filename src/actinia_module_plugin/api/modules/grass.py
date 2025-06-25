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

* List all modules
* Describe single module
"""

__license__ = "Apache-2.0"
__author__ = "Anika Weinmann, Carmen Tawalika, Julia Haas"
__copyright__ = "Copyright 2019 - 2022, mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"


from flask import jsonify, make_response, request
from flask_restful_swagger_2 import swagger
from actinia_rest_lib.resource_base import ResourceBase

from actinia_module_plugin.apidocs import modules
from actinia_module_plugin.core.filter import filter
from actinia_module_plugin.core.modules.grass import createModuleList
from actinia_module_plugin.core.modules.grass import createModuleUserList
from actinia_module_plugin.core.modules.grass import createGrassModule
from actinia_module_plugin.core.modules.grass import createFullModuleList
from actinia_module_plugin.core.modules.grass import installGrassAddon
from actinia_module_plugin.core.modules.accessible_modules_kvdb_interface import (
    addGrassAddonToModuleListKvdb,
)
from actinia_module_plugin.model.modules import ModuleList
from actinia_module_plugin.model.responseModels import (
    SimpleStatusCodeResponseModel,
)


class ListModules(ResourceBase):
    """List all GRASS modules"""

    @swagger.doc(modules.listModules_get_docs)
    def get(self):
        """Get a list of all GRASS GIS modules."""

        module_list = createModuleList(self)
        if self.user_role == "user" or self.user_role == "guest":
            # admins have access to all modules
            user_list = createModuleUserList(self)
            final_list = [m for m in module_list if m["id"] in user_list]
        else:
            final_list = module_list
        final_list = filter(final_list)

        if "record" in request.args:
            if request.args["record"] == "full":
                final_list = createFullModuleList(self, final_list)

        return make_response(
            jsonify(ModuleList(status="success", processes=final_list)), 200
        )


class DescribeModule(ResourceBase):
    """
    Definition for endpoint @app.route('grass_modules/<grassmodule>') to
    desctibe one module

    Contains HTTP GET endpoint
    Contains swagger documentation
    """

    @swagger.doc(modules.describeGrassModule_get_docs)
    def get(self, grassmodule):
        """Describe a GRASS GIS module."""

        try:
            grass_module = createGrassModule(self, grassmodule)
            return make_response(jsonify(grass_module), 200)
        except Exception:
            res = jsonify(
                SimpleStatusCodeResponseModel(
                    status=404,
                    message='Error looking for module "' + grassmodule + '".',
                )
            )
            return make_response(res, 404)

    def post(self, grassmodule):
        """Install an official GRASS GIS Addon."""

        response = installGrassAddon(self, grassmodule)

        if response["status"] == "finished":
            addGrassAddonToModuleListKvdb(self, grassmodule)
            msg = "Successfully installed GRASS addon " + grassmodule + "."
            status_code = 201
        else:
            msg = "Error installing GRASS addon " + grassmodule + "."
            status_code = 400

        res = jsonify(
            SimpleStatusCodeResponseModel(status=status_code, message=msg)
        )
        return make_response(res, status_code)
