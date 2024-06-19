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
