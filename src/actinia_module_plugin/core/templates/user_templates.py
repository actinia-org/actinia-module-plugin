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


Process Chain Template Management
Kvdb CRUD for user templates
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2021, mundialis"
__maintainer__ = "Carmen Tawalika"


from actinia_core.core.common.config import Configuration

from actinia_module_plugin.core.templates.user_templates_kvdb_interface import (
    kvdb_actinia_template_interface,
)


def connect():
    """This method initializes the connection with kvdb."""
    conf = Configuration()
    try:
        conf.read()
    except Exception:
        pass

    server = conf.KVDB_SERVER_URL
    port = conf.KVDB_SERVER_PORT
    if conf.KVDB_SERVER_PW:
        kvdb_password = conf.KVDB_SERVER_PW
    else:
        kvdb_password = None

    kvdb_actinia_template_interface.connect(
        host=server, port=port, password=kvdb_password
    )

    return kvdb_actinia_template_interface


def readAll():
    """
    Get all actinia templates from kvdb database
    """
    kvdb_actinia_template_interface = connect()
    actinia_template = kvdb_actinia_template_interface.list_all_ids()

    return actinia_template


def createTemplate(pc_tpl):
    """
    Insert actinia template into database
    """
    kvdb_actinia_template_interface = connect()
    actinia_template = kvdb_actinia_template_interface.create(pc_tpl)

    return actinia_template


def readTemplate(template_id):
    """
    Get actinia template by id
    """
    kvdb_actinia_template_interface = connect()
    actinia_template = kvdb_actinia_template_interface.read(template_id)

    return actinia_template


def updateTemplate(template_id, pc_tpl):
    """
    Update actinia template by id
    """
    kvdb_actinia_template_interface = connect()
    actinia_template = kvdb_actinia_template_interface.update(
        template_id, pc_tpl
    )

    return actinia_template


def deleteTemplate(template_id):
    """
    Delete actinia template by id
    """
    kvdb_actinia_template_interface = connect()
    actinia_template = kvdb_actinia_template_interface.delete(template_id)

    return actinia_template
