#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2023 mundialis GmbH & Co. KG

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Fumctions for process chain template parameters
"""

__author__ = "Carmen Tawalika, Anika Weinmann"
__copyright__ = "2018-2023 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


from jinja2 import meta, nodes

from re import findall as re_findall

from actinia_module_plugin.resources.templating import pcTplEnv


def find_filters(ast):
    """
    Find all the nodes of a given type. If the type is a tuple,
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
    """
    Return variables that have filters, along with their filters. Might
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


def get_template_default_values(parsed_content):
    """Function to find default variables from processchain"""
    default_vars = []
    filtered_vars = filtered_variables(parsed_content)
    for filtered_var in filtered_vars:
        if "default" in filtered_var[1]:
            default_vars.append(filtered_var[0])
    return default_vars


def filter_undef_without_if_statements(tpl_source, undef, not_needed_vars=[]):
    """
    Function to find variables which are only in an if statement and has
    not to be set
    """
    regex_m_all = []
    if "{% if" in tpl_source or "{%- if" in tpl_source:
        for i in undef:
            if i not in not_needed_vars:
                # be careful with { and {{, if you split the line differently
                # here because of linting
                r_str = (
                    rf"{{%.* if {i} is defined .*%}}[\S\n\t\v ]+?"
                    r"{%.* endif .*%}"
                )
                regex_m = re_findall(r_str, tpl_source)
                regex_m_all.extend(regex_m)

        if len(regex_m_all) > 0:
            tpl_source_mod = tpl_source
            for if_part in regex_m_all:
                tpl_source_mod = tpl_source_mod.replace(if_part, "")
            # check if the variable is still a variable in modified template
            undef_mod = get_template_undef(tpl_source_mod)
            for var in undef:
                if var not in not_needed_vars and var not in undef_mod:
                    not_needed_vars.append(var)


def get_not_needed_params(undef, tpl_source, parsed_content=None):
    """
    Function which filters undef parameters to find which are not needed
    because they have a default value or are only inside a if statement
    """

    if parsed_content is None:
        parsed_content = pcTplEnv.parse(tpl_source)

    # find default variables from processchain
    not_needed_vars = get_template_default_values(parsed_content)
    default_len = len(not_needed_vars)

    # find variables which are only in an if statement and has not to be set
    filter_undef_without_if_statements(tpl_source, undef, not_needed_vars)
    if_len = len(not_needed_vars) - default_len

    # return also the reason why the parameters is not needed
    reason = ["default"] * default_len + ["if"] * if_len

    return {key: val for key, val in zip(not_needed_vars, reason)}


def get_template_undef(tpl_source):
    parsed_content = pcTplEnv.parse(tpl_source)
    undef = meta.find_undeclared_variables(parsed_content)
    return undef
