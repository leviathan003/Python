# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'admin_payments_lay.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from clickableFrame import ClickableFrame
from database import ConnectionPool,showAllPayments,updtPaymentsData,deletePaymentsData
from EntryChecking import *

class PaymentDataRetrievalThread(QtCore.QThread):
    dataRetrieved = QtCore.pyqtSignal(object)
    retrievalComplete = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(PaymentDataRetrievalThread, self).__init__(parent)

    def run(self):
        try:
                pool = ConnectionPool(5, 'hms_database.db')
                data = showAllPayments(pool)
                self.dataRetrieved.emit(data)
        except Exception as e:
            print(e)

class UpdateDelPaymentDataThread(QtCore.QThread):
    operationComplete = QtCore.pyqtSignal()
    def __init__(self,data,flag,parent=None):
        super(UpdateDelPaymentDataThread, self).__init__(parent)
        self.flag=flag
        self.data=data
    def run(self):
        try:
                pool = ConnectionPool(5, 'hms_database.db')
                if(self.flag==1):
                     updtPaymentsData(pool,self.data)
                elif(self.flag==2):
                     deletePaymentsData(pool,self.data)
                self.operationComplete.emit()

        except Exception as e:
            print(e)

class Admin_payments(object):
    
    def __init__(self):
        self.tablePaymentsDet = QtWidgets.QTableWidget()
        self.payIdEntry = QtWidgets.QTextEdit()
        self.invoiceIdEntry = QtWidgets.QTextEdit()
        self.itemNoEntry = QtWidgets.QTextEdit()
        self.totalCostEntry = QtWidgets.QTextEdit()
        self.dateofIssueEntry = QtWidgets.QTextEdit()
        self.timeofIssueEntry = QtWidgets.QTextEdit()
        self.payments_data_thread = PaymentDataRetrievalThread()
        self.payments_data_thread.dataRetrieved.connect(self.updatePaymentsTable)
        self.payments_data_thread.start()

    def backHome(self):
        from Admin_homepage_lay import Admin_home_lay
        self.window = QtWidgets.QMainWindow()
        self.ui = Admin_home_lay()
        self.ui.setupUi(self.window)
        self.window.show()
        self.admin_activity.close()

    def updatePaymentsTable(self,data):
        self.payments_data_thread.retrievalComplete.connect(self.payments_data_thread.quit)
        for row_number, row_data in enumerate(data):
            self.tablePaymentsDet.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(column_data))
                self.tablePaymentsDet.setItem(row_number, column_number, item)

    def showWarningMessage(self,message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setWindowTitle("Warning")
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()

    def verifyUpdtData(self,data):
        if not checkEmptyFields(data):
                self.showWarningMessage("All Fields are mandatory!!")
        else:
             if not checkNumericalData(data[0]) or not checkNumericalData(data[1]) or not checkNumericWith0(data[2]) or not checkNumericWith0(data[3]):
                self.showWarningMessage("Either Payment ID or Invoice ID not numerical!!")
             else:
                if checkLicenseNumber(data[0],self.tablePaymentsDet) and checkInvoiceNumber(data[1],self.tablePaymentsDet):
                        return True
                else:
                        self.showWarningMessage("Either Payment ID or Invoice ID not unique!!")
                         

    def updtData(self):
        data = (self.payIdEntry.toPlainText().strip(),self.invoiceIdEntry.toPlainText().strip(),
                self.itemNoEntry.toPlainText().strip(),self.totalCostEntry.toPlainText().strip(),
                self.dateofIssueEntry.toPlainText().strip(),self.timeofIssueEntry.toPlainText().strip())
        row = getSelectedRowData(self.tablePaymentsDet)
        if row is not None:
                if self.verifyUpdtData(data):
                        data = (self.payIdEntry.toPlainText().strip(),self.invoiceIdEntry.toPlainText().strip(),
                        self.itemNoEntry.toPlainText().strip(),self.totalCostEntry.toPlainText().strip(),
                        self.dateofIssueEntry.toPlainText().strip(),self.timeofIssueEntry.toPlainText().strip(),
                        str(row[0]))
                        self.payments_del_updt_thread = UpdateDelPaymentDataThread(data,flag=1)
                        self.payments_del_updt_thread.start()
                        self.payments_del_updt_thread.operationComplete.connect(self.refreshTable)
                else:
                     self.showWarningMessage("Operation Failed!!")
        else:
             self.showWarningMessage("No record selected!!")
    
    def delData(self):
        row = getSelectedRowData(self.tablePaymentsDet)
        if row is not None:
                selected_id_no = row[0]
                self.payments_del_updt_thread = UpdateDelPaymentDataThread(selected_id_no,flag=2)
                self.payments_del_updt_thread.start()
                self.payments_del_updt_thread.operationComplete.connect(self.refreshTable)
        else:
             self.showWarningMessage("Please select record!!")  

    def refreshTable(self):
        self.tablePaymentsDet.clearContents()
        self.tablePaymentsDet.setRowCount(0)
        self.doc_data_thread = PaymentDataRetrievalThread()
        self.doc_data_thread.dataRetrieved.connect(self.updatePaymentsTable)
        self.doc_data_thread.start()    

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 701)
        MainWindow.showMaximized()
        self.admin_activity = MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.header_frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.header_frame.sizePolicy().hasHeightForWidth())
        self.header_frame.setSizePolicy(sizePolicy)
        self.header_frame.setMinimumSize(QtCore.QSize(1280, 100))
        self.header_frame.setMaximumSize(QtCore.QSize(16777215, 100))
        self.header_frame.setStyleSheet("background-color:rgb(0, 85, 127);")
        self.header_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.header_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.header_frame.setObjectName("header_frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.header_frame)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.logo_frame = ClickableFrame(self.header_frame)
        self.logo_frame.setMinimumSize(QtCore.QSize(80, 50))
        self.logo_frame.setMaximumSize(QtCore.QSize(100, 16777215))
        self.logo_frame.setStyleSheet("background-color:transparent;\n"
"margin-top:6px;\n"
"margin-bottom:0px;")
        self.logo_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.logo_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.logo_frame.setObjectName("logo_frame")
        self.logo_frame.clicked.connect(self.backHome)
        self.backBtn = QtWidgets.QLabel(self.logo_frame)
        self.backBtn.setGeometry(QtCore.QRect(20, 10, 61, 71))
        self.backBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.backBtn.setStyleSheet("")
        self.backBtn.setText("")
        self.backBtn.setPixmap(QtGui.QPixmap(":/reosurces_logo/back-svgrepo-com.svg"))
        self.backBtn.setScaledContents(True)
        self.backBtn.setAlignment(QtCore.Qt.AlignCenter)
        self.backBtn.setObjectName("backBtn")
        self.horizontalLayout.addWidget(self.logo_frame)
        self.title_frame = QtWidgets.QFrame(self.header_frame)
        self.title_frame.setMinimumSize(QtCore.QSize(1280, 0))
        font = QtGui.QFont()
        font.setPointSize(42)
        self.title_frame.setFont(font)
        self.title_frame.setStyleSheet("background-color:transparent;")
        self.title_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.title_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.title_frame.setObjectName("title_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.title_frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title_label = QtWidgets.QLabel(self.title_frame)
        self.title_label.setMinimumSize(QtCore.QSize(800, 0))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("color:#fff;")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")
        self.verticalLayout.addWidget(self.title_label, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout.addWidget(self.title_frame)
        self.verticalLayout_2.addWidget(self.header_frame)
        self.frame_15 = QtWidgets.QFrame(self.centralwidget)
        self.frame_15.setMaximumSize(QtCore.QSize(16777215, 80))
        self.frame_15.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_15.setObjectName("frame_15")
        self.verticalLayout_22 = QtWidgets.QVBoxLayout(self.frame_15)
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.activityNameDisp = QtWidgets.QLabel(self.frame_15)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.activityNameDisp.setFont(font)
        self.activityNameDisp.setStyleSheet("color:rgb(0, 85, 127);")
        self.activityNameDisp.setObjectName("activityNameDisp")
        self.verticalLayout_22.addWidget(self.activityNameDisp, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addWidget(self.frame_15)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setContentsMargins(15, 9, 15, -1)
        self.gridLayout_2.setHorizontalSpacing(15)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setStyleSheet("BACKGROUND-COLOR:#c8cbcf;\n"
"BORDER-RADIUS:5PX;")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_4 = QtWidgets.QFrame(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.frame_4.setFont(font)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_3.addWidget(self.frame_4)
        self.frame_5 = QtWidgets.QFrame(self.frame_3)
        self.frame_5.setStyleSheet("padding-right:2px;\n"
"padding-left:2px;")
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_5)
        self.gridLayout.setHorizontalSpacing(25)
        self.gridLayout.setObjectName("gridLayout")
        self.invoiceIdEntry = QtWidgets.QTextEdit(self.frame_5)
        self.invoiceIdEntry.setMaximumSize(QtCore.QSize(200, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.invoiceIdEntry.setFont(font)
        self.invoiceIdEntry.setStyleSheet("background-color:white;")
        self.invoiceIdEntry.setObjectName("invoiceIdEntry")
        self.gridLayout.addWidget(self.invoiceIdEntry, 0, 3, 1, 1)
        self.itemNoEntry = QtWidgets.QTextEdit(self.frame_5)
        self.itemNoEntry.setMaximumSize(QtCore.QSize(200, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.itemNoEntry.setFont(font)
        self.itemNoEntry.setStyleSheet("background-color:white;")
        self.itemNoEntry.setObjectName("itemNoEntry")
        self.gridLayout.addWidget(self.itemNoEntry, 2, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 3, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 3, 2, 1, 1)
        self.timeofIssueEntry = QtWidgets.QTextEdit(self.frame_5)
        self.timeofIssueEntry.setMaximumSize(QtCore.QSize(200, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.timeofIssueEntry.setFont(font)
        self.timeofIssueEntry.setStyleSheet("background-color:white;")
        self.timeofIssueEntry.setObjectName("timeofIssueEntry")
        self.gridLayout.addWidget(self.timeofIssueEntry, 3, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 2, 1, 1)
        self.dateofIssueEntry = QtWidgets.QTextEdit(self.frame_5)
        self.dateofIssueEntry.setMaximumSize(QtCore.QSize(200, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dateofIssueEntry.setFont(font)
        self.dateofIssueEntry.setStyleSheet("background-color:white;")
        self.dateofIssueEntry.setObjectName("dateofIssueEntry")
        self.gridLayout.addWidget(self.dateofIssueEntry, 3, 1, 1, 1)
        self.totalCostEntry = QtWidgets.QTextEdit(self.frame_5)
        self.totalCostEntry.setMaximumSize(QtCore.QSize(200, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.totalCostEntry.setFont(font)
        self.totalCostEntry.setStyleSheet("background-color:white;")
        self.totalCostEntry.setObjectName("totalCostEntry")
        self.gridLayout.addWidget(self.totalCostEntry, 2, 3, 1, 1)
        self.payIdEntry = QtWidgets.QTextEdit(self.frame_5)
        self.payIdEntry.setMaximumSize(QtCore.QSize(200, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.payIdEntry.setFont(font)
        self.payIdEntry.setStyleSheet("background-color:white;")
        self.payIdEntry.setObjectName("payIdEntry")
        self.gridLayout.addWidget(self.payIdEntry, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.frame_5)
        self.gridLayout_2.addWidget(self.frame_3, 0, 1, 1, 2)
        self.delPaymentsBtn = QtWidgets.QPushButton(self.frame)
        self.delPaymentsBtn.setMinimumSize(QtCore.QSize(200, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.delPaymentsBtn.setFont(font)
        self.delPaymentsBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.delPaymentsBtn.setStyleSheet("background-color:rgb(0, 85, 127);\n"
"COLOR:WHITE;\n"
"BORDER-RADIUS:5PX")
        self.delPaymentsBtn.setObjectName("delDocBtn")
        self.gridLayout_2.addWidget(self.delPaymentsBtn, 2, 1, 1, 2)
        self.tablePaymentsDet = QtWidgets.QTableWidget(self.frame)
        self.tablePaymentsDet.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tablePaymentsDet.setFont(font)
        self.tablePaymentsDet.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.tablePaymentsDet.setStyleSheet("QHeaderView::section {\n"
"                background-color: #00557d;\n"
"                color: white;\n"
"                font-weight: bold;\n"
"padding:5px;\n"
"            }")
        self.tablePaymentsDet.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tablePaymentsDet.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tablePaymentsDet.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tablePaymentsDet.setShowGrid(True)
        self.tablePaymentsDet.setWordWrap(False)
        self.tablePaymentsDet.setObjectName("tablePaymentsDet")
        self.tablePaymentsDet.setColumnCount(6)
        self.tablePaymentsDet.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setBackground(QtGui.QColor(0, 85, 125))
        self.tablePaymentsDet.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablePaymentsDet.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablePaymentsDet.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablePaymentsDet.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablePaymentsDet.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablePaymentsDet.setHorizontalHeaderItem(5, item)
        self.tablePaymentsDet.horizontalHeader().setCascadingSectionResizes(True)
        self.tablePaymentsDet.horizontalHeader().setDefaultSectionSize(180)
        self.tablePaymentsDet.verticalHeader().setDefaultSectionSize(45)
        self.gridLayout_2.addWidget(self.tablePaymentsDet, 0, 0, 3, 1)
        self.updtPaymentBtn = QtWidgets.QPushButton(self.frame)
        self.updtPaymentBtn.setMinimumSize(QtCore.QSize(200, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.updtPaymentBtn.setFont(font)
        self.updtPaymentBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.updtPaymentBtn.setStyleSheet("background-color:rgb(0, 85, 127);\n"
"COLOR:WHITE;\n"
"BORDER-RADIUS:5PX")
        self.updtPaymentBtn.setObjectName("updtDocBtn")
        self.gridLayout_2.addWidget(self.updtPaymentBtn, 1, 1, 1, 2)
        self.verticalLayout_2.addWidget(self.frame)

        self.updtPaymentBtn.clicked.connect(self.updtData)
        self.delPaymentsBtn.clicked.connect(self.delData)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.title_label.setText(_translate("MainWindow", "HOSPITAL MANAGEMENT SYSTEM"))
        self.activityNameDisp.setText(_translate("MainWindow", "PAYMENTS"))
        self.label.setText(_translate("MainWindow", "PAYMENT FORM"))
        self.label_9.setText(_translate("MainWindow", "DATE OF ISSUE:"))
        self.label_4.setText(_translate("MainWindow", "NO OF ITEMS:"))
        self.label_8.setText(_translate("MainWindow", "TIME OF ISSUE:"))
        self.label_3.setText(_translate("MainWindow", "INVOICE ID:"))
        self.label_7.setText(_translate("MainWindow", "TOTAL :"))
        self.label_2.setText(_translate("MainWindow", "PAYMENT ID:"))
        self.delPaymentsBtn.setText(_translate("MainWindow", "DELETE"))
        self.tablePaymentsDet.setSortingEnabled(True)
        item = self.tablePaymentsDet.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "PAYMENT ID"))
        item = self.tablePaymentsDet.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "INVOICE ID"))
        item = self.tablePaymentsDet.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "NO OF ITEMS "))
        item = self.tablePaymentsDet.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "TOTAL"))
        item = self.tablePaymentsDet.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "DATE OF ISSUE"))
        item = self.tablePaymentsDet.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "TIME OF ISSUE"))
        self.updtPaymentBtn.setText(_translate("MainWindow", "UPDATE"))
import resources_rc
