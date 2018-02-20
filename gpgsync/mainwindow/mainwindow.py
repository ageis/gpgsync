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

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app, common, debug=False):
        super(MainWindow, self).__init__()
        self.app = app
        self.common = common
        self.debug = debug

        self.log('__init__')

        self.system = platform.system()

        self.setWindowTitle('GPG Sync')
        self.setWindowIcon(common.get_icon())

        # Window header
        header_logo = QtGui.QImage(self.common.get_resource_path('gpgsync-32x32.png'))
        header_logo_label = QtWidgets.QLabel()
        header_logo_label.setPixmap(QtGui.QPixmap.fromImage(header_logo))
        header_label = QtWidgets.QLabel('GPG Sync')
        header_label.setStyleSheet('QLabel { font-size: 20px; font-weight: bold; }')
        header_layout = QtWidgets.QHBoxLayout()
        header_layout.addWidget(header_logo_label)
        header_layout.addWidget(header_label)
        header_layout.addStretch()

        # Window layout
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(header_layout)
        layout.addStretch()
        central_widget = QtWidgets.QWidget()
        central_widget.setStyleSheet('QWidget { background-color: #ffffff; }')
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.show()

    def log(self, msg):
        if self.debug:
            print("[MainWindow] {}".format(msg))
