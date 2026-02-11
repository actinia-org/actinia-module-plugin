#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SPDX-FileCopyrightText: (c) 2018-2025 by mundialis GmbH & Co. KG

SPDX-License-Identifier: Apache-2.0

Template Environments
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-present mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


from jinja2 import Environment, PackageLoader, FileSystemLoader

from actinia_module_plugin.resources.config import PCTEMPLATECONFIG

# this environment is used for all cases where individual templates are loaded
tplEnv = Environment(
    loader=PackageLoader("actinia_module_plugin", "templates")
)

# this environment is used for process chain templates only
pcTplEnv = Environment(
    # loader=PackageLoader('actinia_module_plugin', 'templates/pc_templates')
    loader=FileSystemLoader(PCTEMPLATECONFIG.pathfile)
)
