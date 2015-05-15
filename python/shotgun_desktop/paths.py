# Copyright (c) 2015 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import sys
import urlparse


class NoPipelineConfigEntityError(Exception):
    """ Error raised when the PipelineConfiguration entity is not available. """
    pass


def get_shotgun_app_root():
    """ returns where the shotgun app is installed """
    if sys.platform == "darwin":
        args = [os.path.dirname(__file__)] + [".."] * 5
        shotgun_root = os.path.abspath(os.path.join(*args))
    elif sys.platform == "win32":
        shotgun_root = os.path.abspath(os.path.dirname(sys.prefix))
    elif sys.platform.startswith("linux"):
        shotgun_root = os.path.abspath(os.path.dirname(sys.prefix))
    else:
        raise NotImplementedError("Unsupported platform: %s" % sys.platform)

    return shotgun_root


def get_python_path():
    """ returns the path to the default python interpreter """
    if sys.platform == "darwin":
        python = os.path.join(sys.prefix, "bin", "python")
    elif sys.platform == "win32":
        python = os.path.join(sys.prefix, "python.exe")
    elif sys.platform.startswith("linux"):
        python = os.path.join(sys.prefix, "bin", "python")
    return python


def get_default_site_config_root(connection):
    """ return the path to the default configuration for the site """
    # find what path field from the entity we need
    if sys.platform == "darwin":
        plat_key = "mac_path"
    elif sys.platform == "win32":
        plat_key = "windows_path"
    elif sys.platform.startswith("linux"):
        plat_key = "linux_path"
    else:
        raise RuntimeError("unknown platform: %s" % sys.platform)

    # interesting fields to return
    fields = ["id", "code", "windows_path", "mac_path", "linux_path"]

    # Toolkit may not have been turned on, check that the PipelineConfiguration entity is available
    pc_schema = connection.schema_entity_read().get("PipelineConfiguration")
    if pc_schema is None:
        raise NoPipelineConfigEntityError()

    pc = connection.find_one(
        "PipelineConfiguration",
        [
            ["project.Project.name", "is", "Template Project"],
            ["project.Project.layout_project", "is", None],
        ],
        fields=fields)

    # see if we found a pipeline configuration
    if pc is not None and pc.get(plat_key, ""):
        # path is already set for us, just return it
        return (str(pc[plat_key]), pc)

    # get operating system specific root
    if sys.platform == "darwin":
        pc_root = os.path.expanduser("~/Library/Application Support/Shotgun")
    elif sys.platform == "win32":
        pc_root = os.path.join(os.environ["APPDATA"], "Shotgun")
    elif sys.platform.startswith("linux"):
        pc_root = os.path.expanduser("~/.shotgun")

    # add on site specific postfix
    site = __get_site_from_connection(connection)
    pc_root = os.path.join(pc_root, site, "site")

    return (str(pc_root), pc)


def __get_site_from_connection(connection):
    """ return the site from the information in the connection """
    # grab just the non-port part of the netloc of the url
    # eg site.shotgunstudio.com
    site = urlparse.urlparse(connection.base_url)[1].split(":")[0]
    return site
