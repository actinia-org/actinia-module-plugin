#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SPDX-FileCopyrightText: (c) 2021-2025 by mundialis GmbH & Co. KG

SPDX-License-Identifier: Apache-2.0

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
