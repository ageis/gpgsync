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
import queue, platform
from PyQt5 import QtCore, QtWidgets

class SysTray(QtWidgets.QSystemTrayIcon):
    quit_signal = QtCore.pyqtSignal()

    def __init__(self, common):
        super(SysTray, self).__init__()
        self.common = common
        self.common.log('SysTray', '__init__')

        self.setIcon(self.common.systray_icon)

        # Menu
        self.menu = QtWidgets.QMenu()
        self.quit_act = self.menu.addAction('Quit')
        self.quit_act.triggered.connect(self.clicked_quit)

        self.setContextMenu(self.menu)
        #self.activated.connect(self.clicked_activated)

        # Show the systray icon
        self.show()

    def clicked_quit(self):
        self.quit_signal.emit()
