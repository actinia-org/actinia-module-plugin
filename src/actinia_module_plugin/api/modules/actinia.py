#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SPDX-FileCopyrightText: (c) 2018-2026 by mundialis GmbH & Co. KG

SPDX-License-Identifier: Apache-2.0

actinia-module viewer
Templates can be stored file based and in kvdb

* List all actinia-modules
* Describe single actinia-module
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2019-2026, mundialis"
__maintainer__ = "Carmen Tawalika"


from flask import jsonify, make_response, request
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

        returns = request.args.get("returns") or None

        try:
            virtual_module = createActiniaModule(self, actiniamodule, returns)
            return make_response(jsonify(virtual_module), 200)
        except Exception:
            msg = 'Error looking for actinia module "' + actiniamodule + '".'
            res = jsonify(
                SimpleStatusCodeResponseModel(status=404, message=msg)
            )
            return make_response(res, 404)
