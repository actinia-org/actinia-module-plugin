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


actinia-module viewer
Templates can be stored file based and in kvdb

* List all actinia-modules
* Describe single actinia-module
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2019, mundialis"
__maintainer__ = "Carmen Tawalika"


from flask import jsonify, make_response
from flask_restful_swagger_2 import swagger
from flask_restful import Resource
import pickle

from actinia_core.core.common.kvdb_interface import enqueue_job
from actinia_core.processing.common.ephemeral_processing_with_export import (
    start_job as start_job_ephemeral_processing_with_export,
)
from actinia_core.rest.base.resource_base import ResourceBase

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


def fillTemplateFromProcessChain(actiniamodule, kwargs):

    pc = actiniamodule
    tpl_source = ""

    # TODO: adjust and reuse
    from actinia_module_plugin.core.processing import (
        fill_env_values,
        check_for_errors,
    )
    ### below imports for core.processing.fillTemplateFromProcessChain
    import json
    from actinia_module_plugin.core.common import (
        get_user_template,
        get_user_template_source,
        get_global_template,
        get_global_template_source,
    )
    from actinia_module_plugin.core.template_parameters import (
        get_not_needed_params,
        get_template_undef,
    )
    from actinia_module_plugin.core.modules.actinia_common import ENV
    from actinia_module_plugin.resources.logging import log
    from actinia_module_plugin.resources.templating import pcTplEnv

    ### below all same inside core.processing.fillTemplateFromProcessChain
    # first see if a user template exists
    tpl = get_user_template(pc)
    tpl_source = get_user_template_source(pc)
    if tpl is False:
        # then fall back to global filesystem template
        tpl = get_global_template(pc)
        tpl_source = get_global_template_source(pc)

    undef = get_template_undef(tpl_source)
    parsed_content = pcTplEnv.parse(tpl_source)

    fill_env_values(kwargs, undef)

    errors = check_for_errors(undef, parsed_content, tpl_source, kwargs)
    if errors is not None:
        return errors

    pc_template = json.loads(tpl.render(**kwargs).replace("\n", ""))
    ### end all same

    return pc_template["template"]


def preprocess_load_tpl_and_enqueue(
        self, preprocess_kwargs, start_job, actiniamodule):
    """
    This method looks up the stored process chain template.
    Template values are filled according to input values.
    The process chain is then passed to actinia-core.
    """

    # run preprocess again after createModuleList
    rdc = self.preprocess(**preprocess_kwargs)

    if rdc:
        rdc.set_storage_model_to_file()

        # TODO: parse kwargs key from undef above ?
        kwargs = {}
        kwargs["geojson"] = rdc.request_data

        new_pc = fillTemplateFromProcessChain(actiniamodule, kwargs)
        rdc.request_data = new_pc

        enqueue_job(self.job_timeout, start_job, rdc)


class ProcessActiniaModule(ResourceBase):
    """
    Process process chain template as "virtual GRASS module"

    Contains HTTP POST endpoint
    Contains swagger documentation
    """

    # TODO: Define input
    # @swagger.doc(modules.processActiniaModule_post_docs)
    def post(self, actiniamodule):
        """Process an actinia module (process chain template)."""

        preprocess_kwargs = {}
        preprocess_kwargs["has_json"] = True
        # TODO: Currently no project can be read out of request body.
        # Instead it will take the first project listed in actinia module
        # To be sure only write a single project inside template.
        virtual_module = createActiniaModule(self, actiniamodule)
        preprocess_kwargs["project_name"] = virtual_module["projects"][0]

        start_job = start_job_ephemeral_processing_with_export

        preprocess_load_tpl_and_enqueue(
            self, preprocess_kwargs, start_job, actiniamodule)

        html_code, response_model = pickle.loads(self.response_data)
        return make_response(jsonify(response_model), html_code)
