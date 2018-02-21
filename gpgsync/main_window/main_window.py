# -*- coding: utf-8 -*-
"""
GPG Sync
Helps users have up-to-date public keys for everyone in their organization
https://github.com/firstlookmedia/gpgsync
Copyright (C) 2016 First Look Media

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import platform
from PyQt5 import QtCore, QtWidgets, QtGui

from .endpoint_list import EndpointList

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app, common, debug=False):
        super(MainWindow, self).__init__()
        self.debug = debug
        self.log('__init__')

        self.app = app
        self.common = common
        self.system = platform.system()

        # Load version string
        version_file = self.common.get_resource_path('version')
        with open(version_file) as f:
            self.version_string = f.read().strip()

        # Load settings
        self.settings = self.common.Settings(self.common, self.debug)

        # Build the window
        self.setWindowTitle('GPG Sync')
        self.setWindowIcon(common.get_icon())

        # Header
        header_widget = QtWidgets.QWidget()
        header_widget.setStyleSheet('QWidget { background-color: #ffffff; border-radius: 5px; }')
        header_logo = QtGui.QImage(self.common.get_resource_path('gpgsync-32x32.png'))
        header_logo_label = QtWidgets.QLabel()
        header_logo_label.setPixmap(QtGui.QPixmap.fromImage(header_logo))
        header_label = QtWidgets.QLabel('GPG Sync')
        header_label.setStyleSheet('QLabel { font-size: 20px; font-weight: bold; }')
        header_layout = QtWidgets.QHBoxLayout()
        header_layout.addStretch()
        header_layout.addWidget(header_logo_label)
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        header_widget.setLayout(header_layout)

        # Endpoint list
        self.endpoint_list = EndpointList(self.common, self.settings, self.debug)

        # Status bar
        version_label = QtWidgets.QLabel(self.version_string)
        version_label.setStyleSheet('QLabel { color: #666666; }')
        self.status_bar = QtWidgets.QStatusBar()
        self.status_bar.addPermanentWidget(version_label)
        self.setStatusBar(self.status_bar)

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(header_widget)
        layout.addWidget(self.endpoint_list)
        layout.addStretch()
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.show()

    def log(self, msg):
        if self.debug:
            print("[MainWindow] {}".format(msg))
