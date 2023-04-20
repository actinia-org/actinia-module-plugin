#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2018-2021 mundialis GmbH & Co. KG

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Module for shared methods
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-2021 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


import json
from jinja2 import Template, DictLoader, Environment

from actinia_module_plugin.core.templates.user_templates import readTemplate
from actinia_module_plugin.resources.templating import pcTplEnv


def start_job(timeout, func, *args):
    """Execute the provided function in a subprocess
    Args:
        func: The function to call from the subprocess
        *args: The function arguments
    Returns:
    """
    # Just starting the process
    from multiprocessing import Process

    p = Process(target=func, args=args)
    p.start()

    return


def filter_func(name):
    """filter examples out of template folder"""

    if "example" not in name:
        return True
    return False


def get_user_template(name):
    actinia_template = readTemplate(name)
    if actinia_template is False:
        return False
    tpl = Template(json.dumps(actinia_template))

    return tpl


def get_user_template_source(name):
    actinia_template = readTemplate(name)
    tplEnv = Environment(loader=DictLoader({name: actinia_template}))
    tpl_source = tplEnv.loader.get_source(tplEnv, name)[0]

    return tpl_source


def get_global_template_path(name):
    tplPath = name + ".json"

    # change path to template if in subdir
    for i in pcTplEnv.list_templates(filter_func=filter_func):
        if i.split("/")[-1] == tplPath:
            tplPath = i

    return tplPath


def get_global_template(name):
    tplPath = get_global_template_path(name)
    tpl = pcTplEnv.get_template(tplPath)
    return tpl


def get_global_template_source(name):
    tplPath = get_global_template_path(name)
    tpl_source = pcTplEnv.loader.get_source(pcTplEnv, tplPath)[0]
    return tpl_source
