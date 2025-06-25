#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2025 mundialis GmbH & Co. KG

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
__copyright__ = "Copyright 2025, mundialis"
__maintainer__ = "Carmen Tawalika"


from flask import jsonify, make_response
import pickle

from actinia_core.core.common.kvdb_interface import enqueue_job
from actinia_core.processing.common.ephemeral_processing_with_export import (
    start_job as start_job_ephemeral_processing_with_export,
)
from actinia_rest_lib.resource_base import ResourceBase

from actinia_module_plugin.core.common import (
    fillTemplateFromProcessChain,
)
from actinia_module_plugin.core.modules.actinia_common import (
    createActiniaModule,
)
from actinia_module_plugin.core.common import (
    get_user_template_source,
    get_global_template_source,
)
from actinia_module_plugin.core.template_parameters import (
    get_template_undef,
)


def preprocess_load_tpl_and_enqueue(
    self, preprocess_kwargs, start_job, actiniamodule
):
    """
    This method looks up the stored process chain template.
    Template values are filled according to input values.
    The process chain is then passed to actinia-core.
    """

    # run preprocess again after createModuleList
    rdc = self.preprocess(**preprocess_kwargs)

    if rdc:
        rdc.set_storage_model_to_file()

        tpl_source = get_user_template_source(
            actiniamodule
        ) or get_global_template_source(actiniamodule)
        undef = get_template_undef(tpl_source)

        # TODO parse request data when schema is defined
        # Might be close to OGC API processes
        kwargs = {}
        kwargs[next(iter(undef))] = rdc.request_data

        new_pc = fillTemplateFromProcessChain(actiniamodule, kwargs)
        rdc.request_data = new_pc

        enqueue_job(self.job_timeout, start_job, rdc)


class ProcessActiniaModule(ResourceBase):
    """
    Process process chain template as actinia-module.

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
            self, preprocess_kwargs, start_job, actiniamodule
        )

        html_code, response_model = pickle.loads(self.response_data)
        return make_response(jsonify(response_model), html_code)
