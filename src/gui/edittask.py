# Form implementation generated from reading ui file 'edittask.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_EditTaskDialog(object):
    def setupUi(self, EditTaskDialog):
        EditTaskDialog.setObjectName("EditTaskDialog")
        EditTaskDialog.resize(389, 296)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(EditTaskDialog.sizePolicy().hasHeightForWidth())
        EditTaskDialog.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(EditTaskDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.labelTaskSummary = QtWidgets.QLabel(EditTaskDialog)
        self.labelTaskSummary.setObjectName("labelTaskSummary")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelTaskSummary)
        self.lineEditSummary = QtWidgets.QLineEdit(EditTaskDialog)
        self.lineEditSummary.setObjectName("lineEditSummary")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEditSummary)
        self.labelTag = QtWidgets.QLabel(EditTaskDialog)
        self.labelTag.setObjectName("labelTag")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelTag)
        self.comboBoxTags = QtWidgets.QComboBox(EditTaskDialog)
        self.comboBoxTags.setEditable(True)
        self.comboBoxTags.setObjectName("comboBoxTags")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.comboBoxTags)
        self.checkBoxEnableCalendar = QtWidgets.QCheckBox(EditTaskDialog)
        self.checkBoxEnableCalendar.setObjectName("checkBoxEnableCalendar")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.checkBoxEnableCalendar)
        self.labelDue = QtWidgets.QLabel(EditTaskDialog)
        self.labelDue.setObjectName("labelDue")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelDue)
        self.dateEdit = QtWidgets.QDateEdit(EditTaskDialog)
        self.dateEdit.setEnabled(False)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setObjectName("dateEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.dateEdit)
        self.comboBoxCalendars = QtWidgets.QComboBox(EditTaskDialog)
        self.comboBoxCalendars.setObjectName("comboBoxCalendars")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.comboBoxCalendars)
        self.labelCalendars = QtWidgets.QLabel(EditTaskDialog)
        self.labelCalendars.setObjectName("labelCalendars")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelCalendars)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(EditTaskDialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(EditTaskDialog)
        QtCore.QMetaObject.connectSlotsByName(EditTaskDialog)

    def retranslateUi(self, EditTaskDialog):
        _translate = QtCore.QCoreApplication.translate
        EditTaskDialog.setWindowTitle(_translate("EditTaskDialog", "Dialog"))
        self.labelTaskSummary.setText(_translate("EditTaskDialog", "Task Summary"))
        self.labelTag.setText(_translate("EditTaskDialog", "Tag"))
        self.checkBoxEnableCalendar.setText(_translate("EditTaskDialog", "Enable Due Date"))
        self.labelDue.setText(_translate("EditTaskDialog", "Due Date"))
        self.dateEdit.setDisplayFormat(_translate("EditTaskDialog", "MM/dd/yyyy"))
        self.labelCalendars.setText(_translate("EditTaskDialog", "Select a Calendar"))
