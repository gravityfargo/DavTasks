# Form implementation generated from reading ui file 'edittags.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_EditTagDialog(object):
    def setupUi(self, EditTagDialog):
        EditTagDialog.setObjectName("EditTagDialog")
        EditTagDialog.resize(400, 200)
        self.gridLayout = QtWidgets.QGridLayout(EditTagDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=EditTagDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.pushButtonColorPicker = QtWidgets.QPushButton(parent=EditTagDialog)
        self.pushButtonColorPicker.setObjectName("pushButtonColorPicker")
        self.gridLayout.addWidget(self.pushButtonColorPicker, 3, 0, 1, 1)
        self.widgetColorPreview = QtWidgets.QWidget(parent=EditTagDialog)
        self.widgetColorPreview.setObjectName("widgetColorPreview")
        self.gridLayout.addWidget(self.widgetColorPreview, 3, 1, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.labelTags = QtWidgets.QLabel(parent=EditTagDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelTags.setFont(font)
        self.labelTags.setObjectName("labelTags")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelTags)
        self.labelTagSelect = QtWidgets.QLabel(parent=EditTagDialog)
        self.labelTagSelect.setObjectName("labelTagSelect")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelTagSelect)
        self.comboBoxTags = QtWidgets.QComboBox(parent=EditTagDialog)
        self.comboBoxTags.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.comboBoxTags.setEditable(True)
        self.comboBoxTags.setObjectName("comboBoxTags")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.comboBoxTags)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 2)

        self.retranslateUi(EditTagDialog)
        self.buttonBox.accepted.connect(EditTagDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(EditTagDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(EditTagDialog)

    def retranslateUi(self, EditTagDialog):
        _translate = QtCore.QCoreApplication.translate
        EditTagDialog.setWindowTitle(_translate("EditTagDialog", "Dav Tasks - Edit Tags"))
        self.pushButtonColorPicker.setText(_translate("EditTagDialog", " Color"))
        self.labelTags.setText(_translate("EditTagDialog", "Tags Settings"))
        self.labelTagSelect.setText(_translate("EditTagDialog", "Select a Tag"))
