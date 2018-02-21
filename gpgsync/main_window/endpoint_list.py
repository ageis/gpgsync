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
from .endpoint_dialog import EndpointDialog

class EndpointList(QtWidgets.QWidget):
    def __init__(self, common):
        super(EndpointList, self).__init__()
        self.common = common
        self.common.log('EndpointList', '__init__')

        # Endpoint layout
        endpoint_layout = QtWidgets.QHBoxLayout()

        # Buttons
        self.add_button = QtWidgets.QPushButton('Add Endpoint')
        self.add_button.clicked.connect(self.add_endpoint)
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

        self.refresh()

    def refresh(self):
        """
        Redraw all endpoints based on what's in settings
        """
        self.common.log('EndpointList', 'refresh')

        for e in self.common.settings.endpoints:
            self.common.log('EndpointList', str(e))

    def add_endpoint(self):
        """
        Open a new dialog to add an endpoint
        """
        self.common.log('EndpointList', 'add_endpoint')
        d = EndpointDialog(self.common, True)
        d.exec_()
