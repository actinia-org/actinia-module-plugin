#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SPDX-FileCopyrightText: (c) 2018-2021 by mundialis GmbH & Co. KG

SPDX-License-Identifier: Apache-2.0

actinia-module viewer
Module for file based templates which are global
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2019, mundialis"
__maintainer__ = "Carmen Tawalika"


import json

from actinia_module_plugin.core.common import filter_func
from actinia_module_plugin.model.modules import Module
from actinia_module_plugin.resources.templating import pcTplEnv
from actinia_module_plugin.resources.logging import log


def createProcessChainTemplateListFromFileSystem():
    """
    list all stored templates and return as actinia-module list
    """

    pc_list = []
    tpl_list = pcTplEnv.list_templates(filter_func=filter_func)

    for tpl_string in tpl_list:
        tpl = pcTplEnv.get_template(tpl_string)
        try:
            pc_template = json.loads(tpl.render().replace("\n", ""))
        except Exception:
            log.error("Error parsing template " + tpl_string)

        try:
            tpl_id = pc_template["id"]
            description = pc_template["description"]
            categories = ["actinia-module", "global-template"]

            pc_response = Module(
                id=tpl_id, description=description, categories=categories
            )
            pc_list.append(pc_response)

        except KeyError:
            log.warning("Could not read template %s" % pc_template)

    return pc_list
