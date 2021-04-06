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


Module for shared methods
"""

__author__ = "Carmen Tawalika"
__copyright__ = "2018-2021 mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"


def start_job(timeout, func, *args):
    """Execute the provided function in a subprocess
    Args:
        func: The function to call from the subprocess
        *args: The function arguments
    Returns:
    """
    # Just starting the process
    from multiprocessing import Process
    p = Process(target=func, args=args)
    p.start()

    return


def filter_func(name):
    ''' filter examples out of template folder
    '''

    if "example" not in name:
        return True
    return False
