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


GRASS GIS module cache in kvdb
Kvdb interface
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2021, mundialis"
__maintainer__ = "Carmen Tawalika"


import pickle

from actinia_core.core.common.kvdb_base import KvdbBaseInterface


class KvdbActiniaGrassModuleInterface(KvdbBaseInterface):
    """
    The Kvdb GRASS GIS module database interface

    A single GRASS GIS module is stored as Hash with:
        - GRASS GIS module name that must be unique
        - GRASS GIS module dictionary

    In addition is the GRASS GIS module name saved in a hash that contains all
    GRASS GIS module names.
    """

    grass_module_id_hash_prefix = "GRASS-MODULE-ID-HASH-PREFIX::"
    grass_module_id_db = "GRASS-MODULE-ID-DATABASE"

    def __init__(self):
        KvdbBaseInterface.__init__(self)

    def create(self, grass_module):
        """
        Add an grass_module to the grass_module database

        Args:
            grass_module (dict): A GRASS GIS interface description

        Returns:
            bool:
            True is success, False if grass_module is already in database
        """

        grass_module_id = grass_module["id"]

        keyname = self.grass_module_id_hash_prefix + grass_module_id
        exists = self.kvdb_server.exists(keyname)
        if exists == 1 or exists is True:
            return False

        grass_module_bytes = pickle.dumps(grass_module)
        mapping = {
            "grass_module_id": grass_module_id,
            "grass_module": grass_module_bytes,
        }

        lock = self.kvdb_server.lock(name="add_grass_module_lock", timeout=1)
        lock.acquire()
        # First add the grass_module-id to the grass_module id database
        self.kvdb_server.hset(
            self.grass_module_id_db, grass_module_id, grass_module_id
        )

        self.kvdb_server.hset(
            self.grass_module_id_hash_prefix + grass_module_id, mapping=mapping
        )
        lock.release()

        return True

    def read(self, grass_module_id):
        """
        Return the grass_module

        HGET grass_module-id grass_module_group

        Args:
            grass_module_id: The grass_module id

        Returns:
             str:
             The grass_module group
        """

        try:
            grass_module = pickle.loads(
                self.kvdb_server.hget(
                    self.grass_module_id_hash_prefix + grass_module_id,
                    "grass_module",
                )
            )
        except Exception:
            return False

        return grass_module

    def update(self, grass_module_id, grass_module):
        """
        Update the grass_module.

        Renaming an entry is not allowed, only existing entries with the
        same grass_module_id can be updated.

        Args:
            grass_module_id (str): The grass_module id
            grass_module (dict): The grass_module as dictionary

        Returns:
            bool:
            True is success, False if grass_module is not in the database

        """
        keyname = self.grass_module_id_hash_prefix + grass_module_id
        exists = self.kvdb_server.exists(keyname)
        if exists == 0 or exists is False:
            return False

        grass_module_bytes = pickle.dumps(grass_module)
        mapping = {
            "grass_module_id": grass_module_id,
            "grass_module": grass_module_bytes,
        }

        lock = self.kvdb_server.lock(
            name="update_grass_module_lock", timeout=1
        )
        lock.acquire()

        self.kvdb_server.hset(
            self.grass_module_id_hash_prefix + grass_module_id, mapping=mapping
        )

        lock.release()

        return True

    # def delete(self, grass_module_id):
    #     """
    #     Remove an grass_module id from the database

    #     Args:
    #         grass_module_id (str): The grass_module id

    #     Returns:
    #         bool:
    #         True is grass_module exists, False otherwise
    #     """
    #     exists = self.exists(grass_module_id)
    #     if exists == 0 or exists is False:
    #         return False

    #     lock = self.kvdb_server.lock(
    #         name="delete_grass_module_lock", timeout=1)
    #     lock.acquire()
    #     # Delete the entry from the grass_module id database
    #     self.kvdb_server.hdel(self.grass_module_id_db,
    #                            grass_module_id)
    #     # Delete the actual grass_module entry
    #     self.kvdb_server.delete(
    #         self.grass_module_id_hash_prefix + grass_module_id)
    #     lock.release()

    #     return True

    # def list_all_ids(self):
    #     """
    #     List all grass_module id's that are in the database

    #     HKEYS on the grass_module id database

    #     Returns:
    #         list:
    #         A list of all grass_module ids in the database
    #     """
    #     values = []
    #     list = self.kvdb_server.hkeys(self.grass_module_id_db)
    #     for entry in list:
    #         entry = entry.decode()
    #         values.append(entry)

    #     return values

    def exists(self, grass_module_id):
        """
        Check if the grass_module is in the database

        Args:
            grass_module_id (str): The grass_module id

        Returns:
            bool:
            True is grass_module exists, False otherwise
        """
        return self.kvdb_server.exists(
            self.grass_module_id_hash_prefix + grass_module_id
        )


# Create the Kvdb interface instance
kvdb_grass_module_interface = KvdbActiniaGrassModuleInterface()
