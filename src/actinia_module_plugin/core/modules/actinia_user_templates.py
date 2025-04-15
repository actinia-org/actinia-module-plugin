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


actinia-module viewer
Module for templates stored in kvdb which are user defined
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2021, mundialis"
__maintainer__ = "Carmen Tawalika"


from actinia_module_plugin.core.templates.user_templates import readAll
from actinia_module_plugin.core.templates.user_templates import readTemplate
from actinia_module_plugin.model.modules import Module


def createProcessChainTemplateListFromKvdb():
    """
    list all stored templates and return as actinia-module list
    """

    pc_list = []
    tpl_list = readAll()

    for tpl_string in tpl_list:
        tpl = readTemplate(tpl_string)

        tpl_id = tpl["id"]
        description = tpl["description"]
        categories = ["actinia-module", "user-template"]

        pc_response = Module(
            id=tpl_id, description=description, categories=categories
        )
        pc_list.append(pc_response)

    return pc_list
