#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SPDX-FileCopyrightText: (c) 2018-2021 by mundialis GmbH & Co. KG

SPDX-License-Identifier: Apache-2.0

Application entrypoint. Creates Flask app and swagger docs, adds endpoints
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-2021 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


from flask import Flask
from flask_cors import CORS
from flask_restful_swagger_2 import Api

from actinia_module_plugin import endpoints
from actinia_module_plugin.resources.logging import log

app = Flask(__name__)
CORS(app)

apidoc = Api(
    app,
    title="actinia-module-plugin",
    api_spec_url="/latest/api/swagger",
    schemes=["https", "http"],
    consumes=["application/json"],
    description="""Contains module self-description and process-chain-template
                   management and processing.
                   """,
)

endpoints.addEndpoints(app, apidoc)


if __name__ == "__main__":
    # call this for development only with
    # `python -m actinia_module_plugin.main`
    log.debug("starting app in development mode...")
    app.run(debug=True, use_reloader=False)
    # for production environent use application in wsgy.py
