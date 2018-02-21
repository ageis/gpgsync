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

class EndpointDialog(QtWidgets.QDialog):
    def __init__(self, common, new):
        super(EndpointDialog, self).__init__()
        self.common = common
        self.common.log('EndpointDialog', '__init__')

        self.new = new

        # Dialog settings
        self.setModal(True)
        self.setMinimumWidth(450)
        if self.new:
            self.setWindowTitle('Add Endpoint')
        else:
            self.setWindowTitle('Edit Endpoint')

        self.endpoint = None

        # Instructions label
        instructions_label = QtWidgets.QLabel("Each endpoint has an authority key fingerprint and a fingerprints URL. Ask your organization's techie for this info.")
        instructions_label.setWordWrap(True)
        instructions_label.setMinimumHeight(40)

        # Signing key fingerprint
        fingerprint_label = QtWidgets.QLabel("GPG Fingerprint")
        self.fingerprint_edit = QtWidgets.QLineEdit()

        # Fingerprints URL
        url_label = QtWidgets.QLabel("Fingerprints URL")
        self.url_edit = QtWidgets.QLineEdit()
        self.url_edit.setPlaceholderText("https://")

        # Signature URL
        self.sig_url_label = QtWidgets.QLabel()
        self.sig_url_label.setStyleSheet('QLabel { font-style: italic; color: #666666; font-size: 12px; }')
        self.url_edit.textChanged.connect(self.update_sig_url)

        # Keyserver
        keyserver_label = QtWidgets.QLabel("Key server")
        self.keyserver_edit = QtWidgets.QLineEdit()

        # SOCKS5 proxy settings
        self.use_proxy = QtWidgets.QCheckBox()
        self.use_proxy.setText("Load URL through SOCKS5 proxy (e.g. Tor)")
        self.use_proxy.setCheckState(QtCore.Qt.Unchecked)

        proxy_host_label = QtWidgets.QLabel('Host')
        self.proxy_host_edit = QtWidgets.QLineEdit()
        proxy_port_label = QtWidgets.QLabel('Port')
        self.proxy_port_edit = QtWidgets.QLineEdit()

        proxy_hlayout = QtWidgets.QHBoxLayout()
        proxy_hlayout.addWidget(proxy_host_label)
        proxy_hlayout.addWidget(self.proxy_host_edit)
        proxy_hlayout.addWidget(proxy_port_label)
        proxy_hlayout.addWidget(self.proxy_port_edit)

        proxy_vlayout = QtWidgets.QVBoxLayout()
        proxy_vlayout.addWidget(self.use_proxy)
        proxy_vlayout.addLayout(proxy_hlayout)

        proxy_group = QtWidgets.QGroupBox("Proxy Configuration")
        proxy_group.setLayout(proxy_vlayout)

        # Advanced layout
        advanced_layout = QtWidgets.QVBoxLayout()
        advanced_layout.addWidget(keyserver_label)
        advanced_layout.addWidget(self.keyserver_edit)
        advanced_layout.addWidget(proxy_group)
        self.advanced_options = QtWidgets.QGroupBox("Advanced options")
        self.advanced_options.setLayout(advanced_layout)
        self.advanced_options.hide()

        # Toggle advanced button
        self.advanced_toggle_button = QtWidgets.QPushButton('Show advanced options')
        self.advanced_toggle_button.setFlat(True)
        self.advanced_toggle_button.setStyleSheet('QPushButton { color: #3f7fcf; }')
        self.advanced_toggle_button.clicked.connect(self.advanced_toggle)
        advanced_toggle_layout = QtWidgets.QHBoxLayout()
        advanced_toggle_layout.addWidget(self.advanced_toggle_button)
        advanced_toggle_layout.addStretch()

        # Buttons
        self.save_button = QtWidgets.QPushButton('Save')
        self.save_button.setDefault(True)
        self.save_button.clicked.connect(self.save_clicked)
        self.cancel_button = QtWidgets.QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.cancel_clicked)
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(instructions_label)
        layout.addWidget(fingerprint_label)
        layout.addWidget(self.fingerprint_edit)
        layout.addWidget(url_label)
        layout.addWidget(self.url_edit)
        layout.addWidget(self.sig_url_label)
        layout.addWidget(self.advanced_options)
        layout.addLayout(advanced_toggle_layout)
        layout.addStretch()
        layout.addLayout(buttons_layout)

        self.update_sig_url(self.url_edit.text())
        self.setLayout(layout)

    def advanced_toggle(self):
        """
        Show or hide advanced options
        """
        self.common.log('EndpointDialog', 'advanced_toggle')
        if self.advanced_options.isVisible():
            self.advanced_options.hide()
            self.advanced_toggle_button.setText('Show advanced options')
        else:
            self.advanced_options.show()
            self.advanced_toggle_button.setText('Hide advanced options')

        self.adjustSize()

    def update_sig_url(self, text):
        """
        When the fingerprints URL changes, update the signature URL too
        """
        if text != '':
            self.sig_url_label.show()
            self.sig_url_label.setText("Signature URL: {}.sig".format(text))
            self.adjustSize()
        else:
            self.sig_url_label.hide()

    def save_clicked(self):
        """
        Save button clicked.
        """
        self.common.log('EndpointDialog', 'save_clicked')

        # Get values for endpoint
        fingerprint = self.common.clean_fp(self.fingerprint_edit.text().strip().encode())
        url = self.url_edit.text().strip().encode()
        keyserver = self.keyserver_edit.text().strip().encode()
        use_proxy = self.use_proxy.checkState() == QtCore.Qt.Checked
        proxy_host = self.proxy_host_edit.text().strip().encode()
        proxy_port = self.proxy_port_edit.text().strip().encode()

        """
        # Show loading graphic, and disable all input until it's finished Verifying
        self.toggle_input(False)

        # Run the verifier inside a new thread
        self.verifier = Verifier(self.debug, self.gpg, self.status_q, fingerprint, url, keyserver, use_proxy, proxy_host, proxy_port)
        self.common.log('EndpointDialog', "save_endpoint, adding Verifier thread ({} threads right now)".format(len(self.threads)))
        self.verifier.alert_error.connect(self.edit_endpoint_alert_error)
        self.verifier.success.connect(self.edit_endpoint_save)
        self.verifier.finished.connect(self.clean_threads)
        self.verifier.start()
        """

        self.close()

    def cancel_clicked(self):
        """
        Cancel button clicked.
        """
        self.common.log('EndpointDialog', 'cancel_clicked')
        self.close()
