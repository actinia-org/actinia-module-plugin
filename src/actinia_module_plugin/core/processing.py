#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SPDX-FileCopyrightText: (c) 2018-2025 by mundialis GmbH & Co. KG

SPDX-License-Identifier: Apache-2.0

Module management related to process chain templates
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2019-2025, mundialis"
__maintainer__ = "Carmen Tawalika"


def build_kwargs_for_template_rendering(module):
    """
    This method receives a process chain for an actinia module, isolates
    the received values and returns them so they can be filled into the
    process chain template.
    """
    kwargs = {}
    inOrOutputs = []

    if module.get("inputs") is not None:
        inOrOutputs += module.get("inputs")

    if module.get("outputs") is not None:
        inOrOutputs += module.get("outputs")

    for item in inOrOutputs:
        if (item.get("param") is None) or (item.get("value") is None):
            return None
        key = item["param"]
        val = item["value"]
        kwargs[key] = val

    return kwargs
