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


Process chain template management
CRUD
* Create process chains template
* Read process chain template
* Update process chain template
* Delete process chain template
* List all process chains templates
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2021, mundialis"
__maintainer__ = "Carmen Tawalika"


from flask import jsonify, make_response, request
from flask_restful_swagger_2 import swagger
from actinia_rest_lib.resource_base import ResourceBase

from actinia_module_plugin.apidocs import templates
from actinia_module_plugin.core.templates.user_templates import readAll
from actinia_module_plugin.core.templates.user_templates import createTemplate
from actinia_module_plugin.core.templates.user_templates import readTemplate
from actinia_module_plugin.core.templates.user_templates import updateTemplate
from actinia_module_plugin.core.templates.user_templates import deleteTemplate
from actinia_module_plugin.core.templates.global_templates import getAll
from actinia_module_plugin.core.templates.global_templates import getTemplate
from actinia_module_plugin.model.responseModels import (
    SimpleStatusCodeResponseModel,
)


class ActiniaTemplate(ResourceBase):
    """List all actinia templates (process chain templates)"""

    @swagger.doc(templates.listTemplates_get_docs)
    def get(self):
        """Get a list of all actinia templates (process chain templates)."""
        user_templates_list = readAll()
        global_templates_list = getAll()
        actinia_templates_list = user_templates_list + global_templates_list

        return make_response(jsonify(actinia_templates_list), 200)

    @swagger.doc(templates.createTemplate_post_docs)
    def post(self):
        """Create an actinia template (process chain template)."""
        template_id = request.get_json(force=True)["id"]
        actinia_template = createTemplate(request.get_json(force=True))
        if actinia_template is True:
            msg = 'Successfully created template "' + template_id + '".'
            status_code = 201
        elif actinia_template is False:
            msg = (
                'Error creating template "'
                + template_id
                + '", it already '
                + "exists. Please delete it before or use HTTP PUT to "
                + "update."
            )
            status_code = 400

        res = jsonify(
            SimpleStatusCodeResponseModel(status=status_code, message=msg)
        )
        return make_response(res, status_code)


class ActiniaTemplateId(ResourceBase):
    """Manage actinia templates (process chain templates)"""

    @swagger.doc(templates.readTemplate_get_docs)
    def get(self, template_id):
        """Read an actinia template (process chain template)."""

        msg = 'Error looking for actinia module "' + template_id + '".'
        res = jsonify(SimpleStatusCodeResponseModel(status=404, message=msg))

        try:
            actinia_template = readTemplate(template_id)
            if actinia_template is not False:
                return make_response(jsonify(actinia_template), 200)

            actinia_template = getTemplate(template_id)
            if actinia_template is not False:
                return make_response(jsonify(actinia_template), 200)
            else:
                return make_response(res, 404)
        except Exception:
            return make_response(res, 404)

    @swagger.doc(templates.updateTemplate_put_docs)
    def put(self, template_id):
        """Update an actinia template (process chain template)."""
        res = jsonify(
            SimpleStatusCodeResponseModel(status=404, message="Error")
        )
        try:
            actinia_template = updateTemplate(
                template_id, request.get_json(force=True)
            )
            if actinia_template is not False:
                return make_response(jsonify(actinia_template), 201)
            else:
                return make_response(res, 404)
        except Exception:
            return make_response(res, 404)

    @swagger.doc(templates.deleteTemplate_delete_docs)
    def delete(self, template_id):
        """Delete an actinia template (process chain template)."""
        res = jsonify(
            SimpleStatusCodeResponseModel(status=404, message="Error")
        )
        try:
            actinia_template = deleteTemplate(template_id)
            if actinia_template is True:
                return make_response(jsonify(actinia_template), 200)
            else:
                return make_response(res, 404)
        except Exception:
            return make_response(res, 404)
