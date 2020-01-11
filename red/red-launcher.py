#!/usr/bin/python3
# -*- coding: utf-8 -*-
# vim: ts=4 sts=4 sw=4 et fileencoding=utf8
import os
import sys
import logging
from copy import deepcopy
from redbot.core import data_manager
from redbot.setup import save_config
from redbot.__main__ import main as redbot_main

logger = logging.getLogger("container.main")

def container_setup():
    """RedBot Setup using environment vars and secrets

    Tries to emulate all the functionality of redbot setup but Container
    Runtime friendly. This writes out the config each time assuming the
    container runtime is providing us the correct data.
    """
    print("[CONTAINER-INIT] Setting up config")

    default_dirs = deepcopy(data_manager.basic_config_default)
    default_data_dir = os.environ.get("RED_DATA_DIR", "/app/data")

    if os.environ.get("RED_USE_POSTGRES", "False").lower() == "true":
        logger.info("Setting up using Postgres storage driver")
        driver_cls = drivers.get_driver_class(BackendType.POSTGRES)
    else:
        logger.info("Setting up using JSON storage driver in: {0}".format(default_data_dir))
        driver_cls = drivers.get_driver_class(BackendType.JSON)

    default_dirs["STORAGE_DETAILS"] = driver_cls.get_config_details()

    try:
        name = os.environ["RED_INSTANCE_NAME"]
    except KeyError:
        logger.critical("Mandatory config item 'RED_INSTANCE_NAME' was not provided! Exiting...")
        sys.exit(1)

    if re.fullmatch(r"[a-zA-Z0-9_\-]*", name) is None:
        logger.critical("Invalid name provided, please keep within: [A-Za-z0-9_-]")
        sys.exit(1)

    save_config(name, default_dirs)

def container_config():
    pass

if __name__ == "__main__":
    container_setup()
    container_config()
    # Some environment vars are already pulled by Red:
    #   RED_TOKEN - Discord API Token
    #   
    redbot_main()
