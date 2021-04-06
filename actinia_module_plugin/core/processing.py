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
from jinja2 import meta, nodes
from jinja2 import Template, DictLoader, Environment

from actinia_module_plugin.core.common import filter_func
from actinia_module_plugin.core.templates.user_templates import readTemplate
from actinia_module_plugin.resources.templating import pcTplEnv
from actinia_module_plugin.resources.logging import log


def find_filters(ast):
    """Find all the nodes of a given type.  If the type is a tuple,
    the check is performed for any of the tuple items.
    Function from: https://stackoverflow.com/questions/55275399/how-to-get-variables-along-with-their-filter-name-from-jinja2-template
    """
    for child in ast.iter_child_nodes():
        if isinstance(child, nodes.Filter):
            yield child
        else:
            for result in find_filters(child):
                yield result


def filtered_variables(ast):
    """Return variables that have filters, along with their filters. might
    return duplicate variable names with different filters
    Function from: https://stackoverflow.com/questions/55275399/how-to-get-variables-along-with-their-filter-name-from-jinja2-template
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


def check_for_errors(tpl_source, kwargs):
    # find variables from processchain
    parsed_content = pcTplEnv.parse(tpl_source)
    undef = meta.find_undeclared_variables(parsed_content)

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

    # first see if a user template exists
    try:
        actinia_template = readTemplate(module["module"])
        tplEnv = Environment(loader=DictLoader(
            {module["module"]: actinia_template}))

        tpl_source = tplEnv.loader.get_source(tplEnv, module["module"])[0]
        tpl = Template(json.dumps(actinia_template))

    # then fall back to global filesystem template
    except Exception:
        tpl_file = module["module"] + '.json'
        # change path to template if in subdir
        for i in pcTplEnv.list_templates(filter_func=filter_func):
            if i.split('/')[-1] == tpl_file:
                tpl_file = i

        tpl_source = pcTplEnv.loader.get_source(pcTplEnv, tpl_file)[0]
        tpl = pcTplEnv.get_template(tpl_file)

    errors = check_for_errors(tpl_source, kwargs)
    if errors is not None:
        return errors

    pc_template = json.loads(tpl.render(**kwargs).replace('\n', ''))
    return (pc_template['template']['list'])
