#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SPDX-FileCopyrightText: (c) 2026 by mundialis GmbH & Co. KG

SPDX-License-Identifier: Apache-2.0

Process Chain Template Management
File reader for global templates
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2026, mundialis"
__maintainer__ = "Carmen Tawalika"


from actinia_module_plugin.core.common import filter_func
from actinia_module_plugin.resources.templating import pcTplEnv


# duplicated from global_templates, left as is due to circular references
def getAllGlobalTemplates():
    """
    This method creates a list of all global templates stored as file
    to return the list to the api method listing all templates.
    """
    tpl_list = pcTplEnv.list_templates(filter_func=filter_func)
    tpl_list = [i.replace(".json", "").split("/")[-1] for i in tpl_list]
    return tpl_list


def isGlobalTemplate(template_id):
    """
    This method checks if an input string is an existing template id.
    """
    if template_id in getAllGlobalTemplates():
        return True
    return False
