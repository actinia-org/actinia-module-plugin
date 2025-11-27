#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SPDX-FileCopyrightText: (c) 2018-2021 by mundialis GmbH & Co. KG

SPDX-License-Identifier: Apache-2.0

Test
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2018-2021, mundialis"


import unittest

from actinia_module_plugin.resources.cli import pc2grass


class CliTest(unittest.TestCase):
    def test_cli_pc2grass(self):
        """Test basic cli command"""
        assert pc2grass() is None
