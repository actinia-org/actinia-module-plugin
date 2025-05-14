#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2018-2025 mundialis GmbH & Co. KG

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


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
