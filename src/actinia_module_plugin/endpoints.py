#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SPDX-FileCopyrightText: (c) 2018-2025 by mundialis GmbH & Co. KG

SPDX-License-Identifier: Apache-2.0

Add endpoints to flask app with endpoint definitions and routes
"""

__author__ = "Carmen Tawalika, Anika Weinmann"
__copyright__ = "2018-2025 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


# from flask import current_app, send_from_directory
# import werkzeug

# from actinia_module_plugin.resources.logging import log
from flask_restful_swagger_2 import Resource

from actinia_module_plugin.api.modules.grass import ListModules
from actinia_module_plugin.api.modules.grass import DescribeModule
from actinia_module_plugin.api.modules.actinia import ListProcessChainTemplates
from actinia_module_plugin.api.modules.actinia import (
    DescribeProcessChainTemplate,
)
from actinia_module_plugin.api.modules.actinia_process import (
    ProcessActiniaModule,
)
from actinia_module_plugin.api.modules.combined import ListVirtualModules
from actinia_module_plugin.api.modules.combined import DescribeVirtualModule
from actinia_module_plugin.api.processing import (
    GdiAsyncEphemeralExportResource,
    GdiAsyncPersistentResource,
)

from actinia_module_plugin.api.actinia_templates import ActiniaTemplate
from actinia_module_plugin.api.actinia_templates import ActiniaTemplateId


def get_endpoint_class_name(
    endpoint_class: Resource) -> str:
    """Create the name for the given endpoint class."""
    return endpoint_class.__name__.lower()
    


def create_project_endpoints(apidoc):
    """
    Function to add resources with "projects" inside the endpoint url.

    Args:
        apidoc (flask_restful_swagger_2.Api): Flask api
        
    """

    apidoc.add_resource(
        GdiAsyncEphemeralExportResource,
        "/projects/<string:project_name>/processing_export",
        "/locations/<string:project_name>/processing_export",
        endpoint=get_endpoint_class_name(GdiAsyncEphemeralExportResource),
    )
    apidoc.add_resource(
        GdiAsyncPersistentResource,
        "/projects/<string:project_name>/mapsets/"
        "<string:mapset_name>/processing",
        "/locations/<string:project_name>/mapsets/"
        "<string:mapset_name>/processing",
        endpoint=get_endpoint_class_name(GdiAsyncPersistentResource),
    )


def create_endpoints(flask_api):
    # app = flask_api.app
    apidoc = flask_api

    # @app.route('/')
    # def index():
    #     try:
    #         # flask cannot reach out of current_app (which is actinia_core)
    #         return current_app.send_static_file('index.html')
    #     except werkzeug.exceptions.NotFound:
    #         log.debug('No index.html found. Serving backup.')
    #         return ("""<h1 style='color:red'>actinia</h1>
    #             <a href="swagger.json">API docs</a>""")
    #
    # @app.route('/<path:filename>')
    # def static_content(filename):
    #     # WARNING: all content from folder "static" will be accessible!
    #     return send_from_directory(app.static_folder, filename)

    apidoc.add_resource(ListModules, "/grass_modules")
    apidoc.add_resource(DescribeModule, "/grass_modules/<grassmodule>")

    apidoc.add_resource(ListProcessChainTemplates, "/actinia_modules")
    apidoc.add_resource(
        DescribeProcessChainTemplate, "/actinia_modules/<actiniamodule>"
    )
    apidoc.add_resource(
        ProcessActiniaModule, "/actinia_modules/<actiniamodule>/process"
    )

    apidoc.add_resource(ListVirtualModules, "/modules")
    apidoc.add_resource(DescribeVirtualModule, "/modules/<module>")

    # add deprecated location and project endpoints
    create_project_endpoints(apidoc)

    apidoc.add_resource(ActiniaTemplate, "/actinia_templates")
    apidoc.add_resource(ActiniaTemplateId, "/actinia_templates/<template_id>")

    # apidoc.add_resource(Actinia, '/actinia/<path:actinia_path>')
    # allows "/" inside variable
