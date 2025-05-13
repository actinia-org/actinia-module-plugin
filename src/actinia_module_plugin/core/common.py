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


Module for shared methods
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-2025 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


import json
from jinja2 import Template, DictLoader, Environment
from os import environ as env

from actinia_module_plugin.core.templates.user_templates import readTemplate
from actinia_module_plugin.core.template_parameters import (
    get_not_needed_params,
    get_template_undef,
)
from actinia_module_plugin.resources.logging import log
from actinia_module_plugin.resources.templating import pcTplEnv


ENV = {
    key.replace("TEMPLATE_VALUE_", ""): val
    for key, val in env.items()
    if key.startswith("TEMPLATE_VALUE_")
}


def start_job(timeout, func, *args):
    """
    Execute the provided function in a subprocess

    Args:
        timeout: Timeout parameter
        func: The function to call from the subprocess
        *args: The function arguments

    Returns:
        returns after starting the process
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


def check_for_errors(undef, parsed_content, tpl_source, kwargs):
    """
    This method checks if all placeholders are filled with values and
    returns the placeholder if missing. Exceptions are default values for which
    the given default value can be used and if statements for which the value
    can be empty.
    """
    # find default variables from processchain and variables which are only in
    # an if statement and has not to be set
    not_needed_vars = get_not_needed_params(undef, tpl_source, parsed_content)

    for i in undef:
        # check if undef variables are needed or set in the kwargs
        if i not in kwargs.keys() and i not in not_needed_vars:
            log.error('Required parameter "' + i + '" not in process chain!')
            return i

    return None


def fill_env_values(filled_params, undef):
    """
    This function checks if a undefined variable is set in the environment
    variables and set it in kwargs if not already set.
    """
    if len(ENV) > 0:
        for param in undef:
            if param not in filled_params and param.upper() in ENV:
                filled_params[param] = ENV[param.upper()]


def fillTemplateFromProcessChain(actiniamodulename, kwargs):
    """
    This method receives a process chain name for an actinia module and
    kwargs to fill the template values. It loads the according process
    chain template from kvdb or filesystem. The received values will be
    replaced to be passed to actinia. In case the template has more
    placeholder values than it receives, the missing attribute is
    returned as string.
    """

    pc = actiniamodulename
    tpl_source = ""

    # first see if a user template exists
    tpl = get_user_template(pc)
    tpl_source = get_user_template_source(pc)
    if tpl is False:
        # then fall back to global filesystem template
        tpl = get_global_template(pc)
        tpl_source = get_global_template_source(pc)

    undef = get_template_undef(tpl_source)
    parsed_content = pcTplEnv.parse(tpl_source)

    fill_env_values(kwargs, undef)

    errors = check_for_errors(undef, parsed_content, tpl_source, kwargs)
    if errors is not None:
        return errors

    pc_template = json.loads(tpl.render(**kwargs).replace("\n", ""))
    return pc_template["template"]
