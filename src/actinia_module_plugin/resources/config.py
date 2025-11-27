#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SPDX-FileCopyrightText: (c) 2018-2021 by mundialis GmbH & Co. KG

SPDX-License-Identifier: Apache-2.0

Configuration file
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-2021 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


import configparser
import glob
from pathlib import Path
import os

# config can be overwritten by mounting *.ini files into folders inside
# the config folder.
DEFAULT_CONFIG_PATH = "config"
CONFIG_FILES = [
    str(f) for f in Path(DEFAULT_CONFIG_PATH).glob("**/*.ini") if f.is_file()
]
GENERATED_CONFIG = DEFAULT_CONFIG_PATH + "/actinia-module-plugin.cfg"


class PCTEMPLATECONFIG:
    """Default path for 'templates/pc_templates'"""

    pathfile = "/src/actinia-module-plugin/config/templates/pc_templates"


class LOGCONFIG:
    """Default config for logging"""

    logfile = "actinia-module-plugin.log"
    level = "DEBUG"
    type = "stdout"


class Configfile:
    def __init__(self):
        """
        This class will overwrite the config classes above when config files
        named DEFAULT_CONFIG_PATH/**/*.ini exist.
        On first import of the module it is initialized.
        """
        from actinia_module_plugin.resources.logging import log

        config = configparser.ConfigParser()
        config.read(CONFIG_FILES)

        if len(config) <= 1:
            log.info("Could not find any config file, using default values.")
            return
        log.info("Loading config files: " + str(CONFIG_FILES) + " ...")

        with open(GENERATED_CONFIG, "w") as configfile:
            config.write(configfile)
        log.debug("Configuration written to " + GENERATED_CONFIG)

        # LOGGING
        if config.has_section("LOGCONFIG"):
            if config.has_option("LOGCONFIG", "logfile"):
                LOGCONFIG.logfile = config.get("LOGCONFIG", "logfile")
            if config.has_option("LOGCONFIG", "level"):
                LOGCONFIG.level = config.get("LOGCONFIG", "level")
            if config.has_option("LOGCONFIG", "type"):
                LOGCONFIG.type = config.get("LOGCONFIG", "type")

        # TEMPLATE PATH
        if os.getenv("PCTEMPLATES") is not None:
            PCTEMPLATECONFIG.pathfile = os.getenv("PCTEMPLATES")
        elif config.has_section("PCTEMPLATECONFIG"):
            if config.has_option("PCTEMPLATECONFIG", "pathfile"):
                PCTEMPLATECONFIG.pathfile = config.get(
                    "PCTEMPLATECONFIG", "pathfile"
                )


init = Configfile()
