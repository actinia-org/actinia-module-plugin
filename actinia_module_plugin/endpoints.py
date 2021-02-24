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


Add endpoints to flask app with endpoint definitions and routes
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-2021 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


from flask import current_app, send_from_directory
import werkzeug

from actinia_module_plugin.resources.logging import log

from actinia_module_plugin.api.gmodules.grass import ListModules
from actinia_module_plugin.api.gmodules.grass import DescribeModule
from actinia_module_plugin.api.gmodules.actinia import ListProcessChainTemplates
from actinia_module_plugin.api.gmodules.actinia import DescribeProcessChainTemplate
from actinia_module_plugin.api.gmodules.combined import ListVirtualModules
from actinia_module_plugin.api.gmodules.combined import DescribeVirtualModule
from actinia_module_plugin.api.gdi_processing import \
    GdiAsyncEphemeralExportResource, GdiAsyncPersistentResource


# endpoints loaded if run as actinia-core plugin
def create_endpoints(flask_api):

    app = flask_api.app
    apidoc = flask_api

    @app.route('/')
    def index():
        try:
            return current_app.send_static_file('index.html')
        except werkzeug.exceptions.NotFound:
            log.debug('No index.html found in static folder. Serving backup.')
            # when actinia-module-plugin is installed in single mode, the swagger
            # endpoint would be "latest/api/swagger.json". As api docs exist in
            # single mode, use this fallback for plugin mode.
            return ("""<h1 style='color:red'>actinia-module-plugin</h1>
                <a href="api/v1/swagger.json">API docs</a>""")

    @app.route('/<path:filename>')
    def static_content(filename):
        # WARNING: all content from folder "static" will be accessible!
        return send_from_directory(app.static_folder, filename)

    apidoc.add_resource(ListModules, '/grassmodules')
    apidoc.add_resource(DescribeModule, '/grassmodules/<grassmodule>')

    apidoc.add_resource(ListProcessChainTemplates, '/actiniamodules')
    apidoc.add_resource(DescribeProcessChainTemplate,
                        '/actiniamodules/<actiniamodule>')

    apidoc.add_resource(ListVirtualModules, '/modules')
    apidoc.add_resource(DescribeVirtualModule, '/modules/<module>')

    apidoc.add_resource(
        GdiAsyncEphemeralExportResource,
        '/locations/<string:location_name>/gdi_processing_async_export'
    )

    apidoc.add_resource(
        GdiAsyncPersistentResource,
        '/locations/<string:location_name>/mapsets/<string:mapset_name>/gdi_processing_async'
    )

    # apidoc.add_resource(Actinia, '/actinia/<path:actinia_path>')
    # allows "/" inside variable
