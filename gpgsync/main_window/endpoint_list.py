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
        self.endpoint_layout = QtWidgets.QVBoxLayout()

        # Buttons
        self.add_button = QtWidgets.QPushButton()
        self.add_button.clicked.connect(self.add_clicked)
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addStretch()

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(self.endpoint_layout)
        layout.addStretch()
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.refresh()

    def refresh(self):
        """
        Redraw all endpoints based on what's in settings
        """
        self.common.log('EndpointList', 'refresh')

        # If there are no endpoints yet
        if len(self.common.settings.endpoints) == 0:
            self.add_button.setText('Add First GPG Sync Endpoint')
            self.add_button.setStyleSheet('QPushButton { background-color: #5fa416; color: #ffffff; padding: 10px; border: 0; border-radius: 5px; }')
        else:
            self.add_button.setText('Add')
            self.add_button.setStyleSheet('QPushButton { font-size: 11px; }')

        # Remove all widgets in the endpoint layout
        while self.endpoint_layout.count() > 0:
            item = self.endpoint_layout.takeAt(0)
            self.endpoint_layout.removeItem(item)

        # Add new widgets from the endpoints in settings
        for e in self.common.settings.endpoints:
            widget = self.create_endpoint_widget(e)
            self.endpoint_layout.addWidget(widget)

        self.adjustSize()

    def create_endpoint_widget(self, e):
        """
        Generate an endpoint widget to add to the list
        """
        # Group box for the endpoint
        widget = QtWidgets.QGroupBox()
        uid = self.common.gpg.get_uid(e.fingerprint)
        if uid != '':
            widget.setTitle(uid)
        else:
            keyid = self.common.fp_to_keyid(e.fingerprint).decode()
            widget.setTitle(keyid)

        # Last synced label
        last_synced_label = QtWidgets.QLabel()
        if e.last_checked:
            if e.error:
                last_synced = str(e.last_failed)
            else:
                last_synced = str(e.last_synced)
        else:
            last_synced = 'never'

        if e.error:
            last_synced_label.setText('Last attempted: {}'.format(last_synced))
        else:
            last_synced_label.setText('Last synced: {}'.format(last_synced))

        # Buttons
        button_style = 'QPushButton { font-size: 11px; }'
        edit_button = QtWidgets.QPushButton('Edit')
        edit_button.clicked.connect(lambda: self.edit_clicked(e))
        edit_button.setStyleSheet(button_style)
        delete_button = QtWidgets.QPushButton('Delete')
        delete_button.clicked.connect(lambda: self.delete_clicked(e))
        delete_button.setStyleSheet(button_style)
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(edit_button)
        buttons_layout.addWidget(delete_button)
        buttons_layout.addStretch()

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(last_synced_label)
        layout.addLayout(buttons_layout)
        widget.setLayout(layout)

        return widget

    def add_clicked(self):
        """
        Open a new dialog to add an endpoint
        """
        self.common.log('EndpointList', 'add_endpoint')
        d = EndpointDialog(self.common)
        d.finished.connect(self.refresh)
        d.exec_()

    def edit_clicked(self, e):
        """
        Open a new dialog to edit the endpoint
        """
        self.common.log('EndpointList', 'edit_clicked {}'.format(e.url))

    def delete_clicked(self, e):
        """
        Delete the endpoint
        """
        self.common.log('EndpointList', 'delete_clicked {}'.format(e.url))
        self.common.alert('Are you sure you want to delete this endpoint?', question=True)
