# Form implementation generated from reading ui file 'notificationDialog.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_notificationDialog(object):
    def setupUi(self, notificationDialog):
        notificationDialog.setObjectName("notificationDialog")
        notificationDialog.resize(258, 150)
        self.verticalLayout = QtWidgets.QVBoxLayout(notificationDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelText = QtWidgets.QLabel(notificationDialog)
        self.labelText.setStyleSheet("font: 18pt \"Noto Sans\";")
        self.labelText.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelText.setObjectName("labelText")
        self.verticalLayout.addWidget(self.labelText)
        self.labelDesc = QtWidgets.QLabel(notificationDialog)
        self.labelDesc.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelDesc.setObjectName("labelDesc")
        self.verticalLayout.addWidget(self.labelDesc)

        self.retranslateUi(notificationDialog)
        QtCore.QMetaObject.connectSlotsByName(notificationDialog)

    def retranslateUi(self, notificationDialog):
        _translate = QtCore.QCoreApplication.translate
        notificationDialog.setWindowTitle(_translate("notificationDialog", "Attention"))
        self.labelText.setText(_translate("notificationDialog", "TextLabel"))
        self.labelDesc.setText(_translate("notificationDialog", "TextLabel"))