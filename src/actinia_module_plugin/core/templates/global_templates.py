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


Process Chain Template Management
File reader for global templates
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2021, mundialis"
__maintainer__ = "Carmen Tawalika"


from actinia_module_plugin.core.common import filter_func
from actinia_module_plugin.core.modules.actinia_common import render_template
from actinia_module_plugin.resources.templating import pcTplEnv


def getAll():
    """
    This method creates a list of all global templates stored as file
    to return the list to the api method listing all templates.
    """
    tpl_list = pcTplEnv.list_templates(filter_func=filter_func)
    tpl_list = [i.replace(".json", "").split("/")[-1] for i in tpl_list]
    return tpl_list


def getTemplate(template_id):
    """
    This method uses other core methods to return a rendered template stored
    as file to return it to the api method showing a certain template.
    """
    return render_template(template_id)
