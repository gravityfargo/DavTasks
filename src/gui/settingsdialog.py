# Form implementation generated from reading ui file 'settingsdialog.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DialogSettings(object):
    def setupUi(self, DialogSettings):
        DialogSettings.setObjectName("DialogSettings")
        DialogSettings.resize(504, 235)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogSettings.sizePolicy().hasHeightForWidth())
        DialogSettings.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(DialogSettings)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogSettings)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.labelServer = QtWidgets.QLabel(DialogSettings)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelServer.setFont(font)
        self.labelServer.setObjectName("labelServer")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelServer)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.formLayout.setItem(0, QtWidgets.QFormLayout.ItemRole.FieldRole, spacerItem)
        self.labelURL = QtWidgets.QLabel(DialogSettings)
        self.labelURL.setObjectName("labelURL")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelURL)
        self.lineEditURL = QtWidgets.QLineEdit(DialogSettings)
        self.lineEditURL.setText("")
        self.lineEditURL.setObjectName("lineEditURL")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEditURL)
        self.labelUser = QtWidgets.QLabel(DialogSettings)
        self.labelUser.setObjectName("labelUser")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelUser)
        self.lineEditUser = QtWidgets.QLineEdit(DialogSettings)
        self.lineEditUser.setObjectName("lineEditUser")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEditUser)
        self.labelPass = QtWidgets.QLabel(DialogSettings)
        self.labelPass.setObjectName("labelPass")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelPass)
        self.lineEditPass = QtWidgets.QLineEdit(DialogSettings)
        self.lineEditPass.setObjectName("lineEditPass")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEditPass)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)

        self.retranslateUi(DialogSettings)
        QtCore.QMetaObject.connectSlotsByName(DialogSettings)

    def retranslateUi(self, DialogSettings):
        _translate = QtCore.QCoreApplication.translate
        DialogSettings.setWindowTitle(_translate("DialogSettings", "Settings"))
        self.labelServer.setText(_translate("DialogSettings", "Server Settings"))
        self.labelURL.setText(_translate("DialogSettings", "Server URL"))
        self.lineEditURL.setPlaceholderText(_translate("DialogSettings", "example.com"))
        self.labelUser.setText(_translate("DialogSettings", "Username"))
        self.lineEditUser.setPlaceholderText(_translate("DialogSettings", "Username"))
        self.labelPass.setText(_translate("DialogSettings", "Password"))
        self.lineEditPass.setPlaceholderText(_translate("DialogSettings", "Password"))
