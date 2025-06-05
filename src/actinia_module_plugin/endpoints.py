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
    endpoint_class: Resource,
    projects_url_part: str = "projects",
) -> str:
    """Create the name for the given endpoint class."""
    endpoint_class_name = endpoint_class.__name__.lower()
    if projects_url_part != "projects":
        name = f"{endpoint_class_name}_{projects_url_part}"
    else:
        name = endpoint_class_name
    return name


def create_project_endpoints(apidoc, projects_url_part="projects"):
    """
    Function to add resources with "projects" inside the endpoint url.

    Args:
        apidoc (flask_restful_swagger_2.Api): Flask api
        projects_url_part (str): The name of the projects inside the endpoint
                                 URL; to add deprecated location endpoints set
                                 it to "locations"
    """

    apidoc.add_resource(
        GdiAsyncEphemeralExportResource,
        f"/{projects_url_part}/<string:project_name>/processing_export",
        endpoint=get_endpoint_class_name(
            GdiAsyncEphemeralExportResource, projects_url_part
        ),
    )
    apidoc.add_resource(
        GdiAsyncPersistentResource,
        f"/{projects_url_part}/<string:project_name>/mapsets/"
        "<string:mapset_name>/processing",
        endpoint=get_endpoint_class_name(
            GdiAsyncPersistentResource, projects_url_part
        ),
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
    create_project_endpoints(apidoc, projects_url_part="locations")

    apidoc.add_resource(ActiniaTemplate, "/actinia_templates")
    apidoc.add_resource(ActiniaTemplateId, "/actinia_templates/<template_id>")

    # apidoc.add_resource(Actinia, '/actinia/<path:actinia_path>')
    # allows "/" inside variable
