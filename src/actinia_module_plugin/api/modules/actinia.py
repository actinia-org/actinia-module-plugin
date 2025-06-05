#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2018-2025 mundialis GmbH & Co. KG

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


actinia-module viewer
Templates can be stored file based and in kvdb

* List all actinia-modules
* Describe single actinia-module
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2019-2025, mundialis"
__maintainer__ = "Carmen Tawalika"


from flask import jsonify, make_response
from flask_restful_swagger_2 import swagger
from flask_restful import Resource

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
from actinia_module_plugin.model.modules import ModuleList
from actinia_module_plugin.model.responseModels import (
    SimpleStatusCodeResponseModel,
)


class ListProcessChainTemplates(Resource):
    """List all process chain templates"""

    @swagger.doc(modules.listModules_get_docs)
    def get(self):
        """Get a list of all actinia modules (process chain templates)."""

        pc_list_fs = createProcessChainTemplateListFromFileSystem()
        pc_list_kvdb = createProcessChainTemplateListFromKvdb()
        pc_list = pc_list_fs + pc_list_kvdb

        pc_list = filter(pc_list)

        return make_response(
            jsonify(ModuleList(status="success", processes=pc_list)), 200
        )


class DescribeProcessChainTemplate(ResourceBase):
    """
    Describe process chain template as "virtual GRASS module"

    Contains HTTP GET endpoint
    Contains swagger documentation
    """

    @swagger.doc(modules.describeActiniaModule_get_docs)
    def get(self, actiniamodule):
        """Describe an actinia module (process chain template)."""

        try:
            virtual_module = createActiniaModule(self, actiniamodule)
            return make_response(jsonify(virtual_module), 200)
        except Exception:
            msg = 'Error looking for actinia module "' + actiniamodule + '".'
            res = jsonify(
                SimpleStatusCodeResponseModel(status=404, message=msg)
            )
            return make_response(res, 404)
