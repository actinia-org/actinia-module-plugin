#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SPDX-FileCopyrightText: (c) 2021-2025 by mundialis GmbH & Co. KG

SPDX-License-Identifier: Apache-2.0

Filter for module and template viewer
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2021, mundialis"
__maintainer__ = "Carmen Tawalika"


from flask import request

global family
global tag
global category


def filter(full_list):
    filter_list = full_list

    # INFO: record=full is directly parsed in api method

    if "family" in request.args:
        global family
        family = request.args["family"]
        # d, db, g, i, m, ps, r, r3, t, test, v
        val = family + "."
        filter_list = [i for i in filter_list if str(i["id"]).startswith(val)]

    if "tag" in request.args:
        global tag
        tag = request.args["tag"]
        filter_list = [i for i in filter_list if tag in str(i["categories"])]

    if "category" in request.args:
        global category
        category = request.args["category"]
        filter_list = [
            i for i in filter_list if category in str(i["categories"])
        ]

    return filter_list
