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


Module management related to process chain templates
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2019, mundialis"
__maintainer__ = "Carmen Tawalika"


import json
from jinja2 import nodes

from actinia_module_plugin.core.common import \
     get_user_template, get_user_template_source, \
     get_global_template, get_global_template_source, \
     get_template_undef
from actinia_module_plugin.resources.logging import log
from actinia_module_plugin.resources.templating import pcTplEnv


def find_filters(ast):
    """Find all the nodes of a given type. If the type is a tuple,
    the check is performed for any of the tuple items.
    Function from: https://stackoverflow.com/questions/55275399/how-to-get
    -variables-along-with-their-filter-name-from-jinja2-template
    """
    for child in ast.iter_child_nodes():
        if isinstance(child, nodes.Filter):
            yield child
        else:
            for result in find_filters(child):
                yield result


def filtered_variables(ast):
    """Return variables that have filters, along with their filters. Might
    return duplicate variable names with different filters
    Function from: https://stackoverflow.com/questions/55275399/how-to-get
    -variables-along-with-their-filter-name-from-jinja2-template
    """
    results = []
    for i, node in enumerate(find_filters(ast)):
        filters = []
        f = node
        filters.append(f.name)
        while isinstance(f.node, nodes.Filter):
            f = f.node
            filters.append(f.name)
        filters.reverse()
        results.append((f.node.name, filters))
    return results


def build_kwargs_for_template_rendering(module):
    """This method receives a process chain for an actinia module, isolates
    the received values and returns them so they can be filled into the
    process chain template.
    """
    kwargs = {}
    inOrOutputs = []

    if module.get('inputs') is not None:
        inOrOutputs += module.get('inputs')

    if module.get('outputs') is not None:
        inOrOutputs += module.get('outputs')

    for item in inOrOutputs:
        if (item.get('param') is None) or (item.get('value') is None):
            return None
        key = item['param']
        val = item['value']
        kwargs[key] = val

    return kwargs


def check_for_errors(undef, parsed_content, kwargs):
    """This method checks if all placeholders are filled with values and
    returns the placeholder if missing. Exceptions are default values for which
    the given default value can be used.
    """
    # find default variables from processchain
    default_vars = []
    filtered_vars = filtered_variables(parsed_content)
    for filtered_var in filtered_vars:
        if 'default' in filtered_var[1]:
            default_vars.append(filtered_var[0])

    for i in undef:
        if i not in kwargs.keys() and i not in default_vars:
            log.error('Required parameter "' + i + '" not in process chain!')
            return i

    return None


def fillTemplateFromProcessChain(module):
    """ This method receives a process chain for an actinia module and loads
        the according process chain template from redis or filesystem. The
        received values will be replaced to be passed to actinia. In case the
        template has more placeholder values than it receives, the missing
        attribute is returned as string.
    """

    kwargs = build_kwargs_for_template_rendering(module)
    tpl_source = ""
    pc = module["module"]

    # first see if a user template exists
    tpl = get_user_template(pc)
    tpl_source = get_user_template_source(pc)
    if tpl is False:
        # then fall back to global filesystem template
        tpl = get_global_template(pc)
        tpl_source = get_global_template_source(pc)

    undef = get_template_undef(tpl_source)
    parsed_content = pcTplEnv.parse(tpl_source)

    errors = check_for_errors(undef, parsed_content, kwargs)
    if errors is not None:
        return errors

    pc_template = json.loads(tpl.render(**kwargs).replace('\n', ''))
    return (pc_template['template']['list'])
