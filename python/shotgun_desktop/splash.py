# Copyright (c) 2015 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

from .qt import QtGui, QtCore

from locksmith.Qt.locksmith_splash import LocksmithSplash


def Splash():
    return LocksmithSplash(
        None, QtCore.Qt.WindowStaysOnTopHint, "locksmith desktop"
    )