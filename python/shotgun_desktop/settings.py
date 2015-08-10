# Copyright (c) 2015 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import sys
import os
import ConfigParser

import shotgun_desktop


class Settings(object):
    """
    Reads the optionally configured config.ini file present in the Desktop
    installer package. This file is in the root of the installed application folder on
    Linux and Windows and in Contents/Resources on MacOSX.

    The config.ini should have the following format
    [Login]
    default_login=login
    default_site=site.shotgunstudio.com
    http_proxy=http://www.someproxy.com:3128
    [BrowserIntegration]
    port=9000
    whitelist=*.shotgunstudio.com
    enabled=1
    """

    _LOGIN = "Login"
    _BROWSER_INTEGRATION = "BrowserIntegration"

    def __init__(self):
        """
        Constructor.
        """
        self._global_config = self._load_config(self._get_global_config_location())

    def _get_global_config_location(self):
        """
        :returns: The location of the global configuration file inside the installation directory.
        """
        if "SGTK_DEFAULT_LOGIN_DEBUG_LOCATION" in os.environ:
            return os.environ["SGTK_DEFAULT_LOGIN_DEBUG_LOCATION"]
        elif sys.platform == "darwin":
            return os.path.join(shotgun_desktop.paths.get_shotgun_app_root(), "Contents", "Resources", "config.ini")
        else:
            return os.path.join(shotgun_desktop.paths.get_shotgun_app_root(), "config.ini")

    def _load_config(self, path):
        """
        Loads the configuration at a given location and returns it.

        :param path: Path to the configuration to load.

        :returns: A ConfigParser instance with the contents from the configuration file.
        """
        config = ConfigParser.SafeConfigParser()
        if os.path.exists(path):
            config.read(path)
        return config

    @property
    def default_http_proxy(self):
        """
        :returns: The default proxy
        """
        return self._get_value(self._LOGIN, "http_proxy")

    @property
    def default_site(self):
        return self._get_value(self._LOGIN, "default_site")

    @property
    def default_login(self):
        return self._get_value(self._LOGIN, "default_login")

    @property
    def integration_port(self):
        return self._get_value(self._BROWSER_INTEGRATION, "port", int, 9000)

    @property
    def integration_enabled(self):
        # Any non empty string is True, so convert it to int, which will accept 0 or 1 and then
        # we'll cast the return value to a boolean.
        return bool(self._get_value(self._BROWSER_INTEGRATION, "enabled", int, True))

    @property
    def integration_whitelist(self):
        return self._get_value(self._BROWSER_INTEGRATION, "whitelist", default="*.shotgunstudio.com")

    def _get_value(self, section, key, type_cast=str, default=None):
        if not self._global_config.has_section(section):
            return default
        elif not self._global_config.has_option(section, key):
            return default
        else:
            return type_cast(self._global_config.get(section, key))
