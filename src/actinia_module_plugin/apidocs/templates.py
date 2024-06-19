#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2021 mundialis GmbH & Co. KG

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Documentation objects for process chain template management
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2021 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


import os
import json

from flask_restful_swagger_2 import Schema
from actinia_core.core.common.process_chain import GrassModule

from actinia_module_plugin.model.responseModels import (
    SimpleStatusCodeResponseModel,
)


script_dir = os.path.dirname(os.path.abspath(__file__))
rel_path = "./examples/pc_template.json"
abs_file_path = os.path.join(script_dir, rel_path)
with open(abs_file_path) as jsonfile:
    pc_template_example = json.load(jsonfile)


null = "null"


class ProcessChainTemplate(Schema):
    """Response schema for module"""

    type = "object"
    properties = {
        "id": {
            "type": "string",
            "description": "Unique identifier of the process. ",
        },
        "description": {
            "type": "string",
            "description": "Detailed description to fully explain the entity.",
        },
        "template": {
            "type": "object",
            "description": "The full process chain template.",
            "properties": {
                "list": {
                    "type": "array",
                    "items": GrassModule,
                    "description": "The list of GRASS GIS or actinia modules"
                    " or executables of which the template"
                    " consists.",
                }
            },
        },
    }
    example = pc_template_example


listTemplates_get_docs = {
    "tags": ["Process Chain Template Management"],
    "description": "Get a list of process chain templates. "
    "Minimum required user role: user.",
    "responses": {
        "200": {"description": "This response returns a list of module names"}
    },
}

readTemplate_get_docs = {
    "tags": ["Process Chain Template Management"],
    "parameters": [
        {
            "in": "path",
            "name": "template_id",
            "type": "string",
            "description": "The name of a process chain template",
            "required": True,
        }
    ],
    "description": "Read a process chain template. "
    "Minimum required user role: user.",
    "responses": {
        "200": {
            "description": "This response returns a process chain template.",
            "schema": ProcessChainTemplate,
        },
        "404": {
            "description": "The error message and a detailed log why "
            "describing did not succeeded",
            "schema": SimpleStatusCodeResponseModel,
        },
    },
}


createTemplate_post_docs = {
    "tags": ["Process Chain Template Management"],
    "description": "Create a process chain template. "
    "Minimum required user role: user.",
    "parameters": [
        {
            "in": "body",
            "name": "template",
            "type": "object",
            "schema": ProcessChainTemplate,
            "description": "The process chain template",
            "required": True,
        }
    ],
    "responses": {
        "201": {
            "description": "This response returns True if creation was"
            " successfull."
        },
        "404": {
            "description": "The error message and a detailed log why "
            "creation did not succeeded",
            "schema": SimpleStatusCodeResponseModel,
        },
    },
}

updateTemplate_put_docs = {
    "tags": ["Process Chain Template Management"],
    "parameters": [
        {
            "in": "path",
            "name": "template_id",
            "type": "string",
            "description": "The name of a process chain template",
            "required": True,
        }
    ],
    "description": "Update a process chain template. "
    "Minimum required user role: user.",
    "responses": {
        "201": {
            "description": "This response returns True if update was"
            " successfull."
        },
        "404": {
            "description": "The error message and a detailed log why "
            "update did not succeeded",
            "schema": SimpleStatusCodeResponseModel,
        },
    },
}

deleteTemplate_delete_docs = {
    "tags": ["Process Chain Template Management"],
    "parameters": [
        {
            "in": "path",
            "name": "template_id",
            "type": "string",
            "description": "The name of a process chain template",
            "required": True,
        }
    ],
    "description": "Delete a process chain template. "
    "Minimum required user role: user.",
    "responses": {
        "200": {
            "description": "This response returns True if deletion was"
            " successfull."
        },
        "404": {
            "description": "The error message and a detailed log why "
            "deletion did not succeeded",
            "schema": SimpleStatusCodeResponseModel,
        },
    },
}
