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


actinia-module + grass-module viewer
Templates can be stored file based and in kvdb

* List all GRASS GIS modules and actinia-modules
* Describe single module
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2019, mundialis"
__maintainer__ = "Carmen Tawalika"


from flask import jsonify, make_response, request
from flask_restful_swagger_2 import swagger
from actinia_rest_lib.resource_base import ResourceBase

from actinia_module_plugin.apidocs import modules
from actinia_module_plugin.core.filter import filter
from actinia_module_plugin.core.modules.actinia_global_templates import (
    createProcessChainTemplateListFromFileSystem,
)
from actinia_module_plugin.core.modules.actinia_user_templates import (
    createProcessChainTemplateListFromKvdb,
)
from actinia_module_plugin.core.modules.actinia_common import (
    createActiniaModule,
)
from actinia_module_plugin.core.modules.grass import createModuleList
from actinia_module_plugin.core.modules.grass import createModuleUserList
from actinia_module_plugin.core.modules.grass import createGrassModule
from actinia_module_plugin.core.modules.grass import createFullModuleList
from actinia_module_plugin.model.modules import ModuleList
from actinia_module_plugin.model.responseModels import (
    SimpleStatusCodeResponseModel,
)


class ListVirtualModules(ResourceBase):
    """List all GRASS GIS modules and process chain templates"""

    @swagger.doc(modules.listModules_get_docs)
    def get(self):
        """Get a list of all modules."""

        grass_list = createModuleList(self)
        if self.user_role == "user" or self.user_role == "guest":
            # admins have access to all modules
            user_list = createModuleUserList(self)
            final_grass_list = [m for m in grass_list if m["id"] in user_list]
        else:
            final_grass_list = grass_list
        final_grass_list = filter(final_grass_list)

        if "record" in request.args:
            if request.args["record"] == "full":
                final_grass_list = createFullModuleList(self, final_grass_list)

        pc_list_fs = createProcessChainTemplateListFromFileSystem()
        pc_list_kvdb = createProcessChainTemplateListFromKvdb()
        module_list = final_grass_list + pc_list_fs + pc_list_kvdb

        module_list = filter(module_list)

        return make_response(
            jsonify(ModuleList(status="success", processes=module_list)), 200
        )


class DescribeVirtualModule(ResourceBase):
    """
    Describe module or process chain template

    Contains HTTP GET endpoint
    Contains swagger documentation
    """

    @swagger.doc(modules.describeModule_get_docs)
    def get(self, module):
        """Describe a module."""

        try:
            try:
                virtual_module = createGrassModule(self, module)
            except Exception:
                virtual_module = createActiniaModule(self, module)
            finally:
                return make_response(jsonify(virtual_module), 200)

        except Exception:
            msg = 'Error looking for module "' + module + '".'
            res = jsonify(
                SimpleStatusCodeResponseModel(status=404, message=msg)
            )
            return make_response(res, 404)
