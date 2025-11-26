#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SPDX-FileCopyrightText: (c) 2018-2021 by mundialis GmbH & Co. KG

SPDX-License-Identifier: Apache-2.0

Common api methods
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-2021 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


from flask_restful_swagger_2 import Schema


class SimpleStatusCodeResponseModel(Schema):
    """Simple response schema to inform about status."""

    type = "object"
    properties = {
        "status": {
            "type": "number",
            "description": "The status code of the request.",
        },
        "message": {
            "type": "string",
            "description": "A short message to describes the status",
        },
    }
    required = ["status", "message"]


simpleResponseExample = SimpleStatusCodeResponseModel(
    status=200, message="success"
)
SimpleStatusCodeResponseModel.example = simpleResponseExample
