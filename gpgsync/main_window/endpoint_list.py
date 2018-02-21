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
from PyQt5 import QtCore, QtWidgets, QtGui

class EndpointList(QtWidgets.QWidget):
    def __init__(self, settings, debug=False):
        super(EndpointList, self).__init__()
        self.debug = debug
        self.log('__init__')

        self.settings = settings

        # Endpoint layout
        endpoint_layout = QtWidgets.QHBoxLayout()

        # Buttons
        self.add_button = QtWidgets.QPushButton('Add Endpoint')
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.add_button)
        button_layout.addStretch()

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(endpoint_layout)
        layout.addStretch()
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def refresh(self):
        """
        Redraw all endpoints based on what's in settings
        """
        pass

    def log(self, msg):
        if self.debug:
            print("[EndpointList] {}".format(msg))
