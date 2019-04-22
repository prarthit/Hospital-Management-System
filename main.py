from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from datetime import date

from functools import partial
import sip

from datetime import timedelta
from datetime import datetime

import sys

import mysql.connector

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="yogislife",
	database="HMS"
)

mycursor = mydb.cursor()

ui,_ = loadUiType('main.ui')
emergency_ui,_ = loadUiType('emergency.ui')
payBill_ui,_= loadUiType('payBill.ui')
appointment_ui,_ = loadUiType('appointment.ui')

class MainApp(QMainWindow, ui):
	def __init__(self):
		QMainWindow.__init__(self)
		ui.setupUi(self, self)
		self.setupUi(self)
		self.setupButtons()

	def setupButtons(self):
		self.pushButton.clicked.connect(self.receptionist)
		self.pushButton_2.clicked.connect(self.infraAdmin)
		self.pushButton_3.clicked.connect(self.financeAdmin)
		self.pushButton_4.clicked.connect(self.showTable)
		self.pushButton_5.clicked.connect(self.showTable)
		self.pushButton_6.clicked.connect(self.showTable)
		self.pushButton_10.clicked.connect(self.backBtn)
		self.pushButton_8.clicked.connect(self.insert)
		self.pushButton_9.clicked.connect(self.update)
		self.pushButton_7.clicked.connect(self.delete)
		self.pushButton_11.clicked.connect(self.backBtn)
		self.pushButton_12.clicked.connect(self.backBtn)
		self.pushButton_13.clicked.connect(self.backBtn)
		self.pushButton_14.clicked.connect(self.backBtn)

	def receptionist(self):
		self.stackedWidget.setCurrentIndex(2);

	def infraAdmin(self):
		self.stackedWidget.setCurrentIndex(3);

	def financeAdmin(self):
		self.stackedWidget.setCurrentIndex(4);

	def backBtn(self):
		currIndex = self.stackedWidget.currentIndex();
		if(currIndex==3 or currIndex==4):
			self.stackedWidget.setCurrentIndex(1);
		elif(currIndex==5):
			self.stackedWidget.setCurrentIndex(self.prevIndex);
		else:
			self.stackedWidget.setCurrentIndex(currIndex-1);

	def nextBtn(self):
		currIndex = self.stackedWidget.currentIndex();
		self.stackedWidget.setCurrentIndex(currIndex + 1);

	def showTable(self):
		_translate = QCoreApplication.translate
		radios = [[1,8,9], [2,10,11,12,13], [3,14,15]]

		currIndex = self.stackedWidget.currentIndex()
		self.prevIndex = currIndex;

		for i in range(len(radios[currIndex - 2])):
			selected_radio = self.findChild(QRadioButton, "radioButton_"+str(radios[currIndex - 2][i]))
			if selected_radio.isChecked():
				self.tableName = selected_radio.text()
				mycursor.execute("SELECT * FROM "+str(self.tableName))
				rows = mycursor.fetchall()
				self.loadTableData(rows)
				break

		if(hasattr(self, 'extraBtn1') and sip.isdeleted(self.extraBtn1)==False):
			self.extraBtn1.deleteLater()
		if(hasattr(self, 'extraBtn2') and sip.isdeleted(self.extraBtn2)==False):
			self.extraBtn2.deleteLater()

		if(self.tableName == "Patient"):
			self.extraBtn1 = QPushButton(self.page_5)
			self.extraBtn1.setGeometry(QRect(270, 380, 141, 40))
			self.extraBtn1.setObjectName("extraBtn1")
			self.extraBtn1.setText(_translate("MainWindow", "Medical History"))
			self.extraBtn1.clicked.connect(self.medicalHistory)

		elif(self.tableName == "Bed_record"):

			self.extraBtn1 = QPushButton(self.page_5)
			self.extraBtn1.setGeometry(QRect(210, 380, 111, 40))
			self.extraBtn1.setObjectName("extraBtn1")
			self.extraBtn2 = QPushButton(self.page_5)
			self.extraBtn2.setGeometry(QRect(340, 380, 131, 40))
			self.extraBtn2.setObjectName("extraBtn2")
			self.extraBtn1.setText(_translate("MainWindow", "Show Bed"))
			self.extraBtn2.setText(_translate("MainWindow", "Pay Bill"))

			self.extraBtn1.clicked.connect(self.showBed)
			self.extraBtn2.clicked.connect(self.payBill)

		elif(self.tableName == "Doctor"):
			self.extraBtn1 = QPushButton(self.page_5)
			self.extraBtn1.setGeometry(QRect(210, 380, 111, 40))
			self.extraBtn1.setObjectName("extraBtn1")
			self.extraBtn2 = QPushButton(self.page_5)
			self.extraBtn2.setGeometry(QRect(340, 380, 131, 40))
			self.extraBtn2.setObjectName("extraBtn2")
			self.extraBtn1.setText(_translate("MainWindow", "Appointment"))
			self.extraBtn2.setText(_translate("MainWindow", "Emergency Alert"))

			self.extraBtn1.clicked.connect(self.appointment)
			self.extraBtn2.clicked.connect(self.emerAlert)
        
		self.stackedWidget.setCurrentIndex(5)

	def loadTableData(self, rows):
		mycursor.execute("SHOW Columns FROM "+str(self.tableName))
		columnsData = mycursor.fetchall()
		self.columnsName = []

		for item in columnsData:
			self.columnsName.append(item[0])

		self.tableWidget.setRowCount(0)
		self.tableWidget.setColumnCount(len(self.columnsName))

		self.tableWidget.setHorizontalHeaderLabels(self.columnsName)

		for row_num, row_data in enumerate(rows):
			self.tableWidget.insertRow(row_num)
			for col_num, data in enumerate(row_data):
				self.tableWidget.setItem(row_num, col_num, QTableWidgetItem(str(data)))

		self.tableWidget.insertRow(len(rows))
		# self.tableWidget.resizeColumnsToContents()
		# self.tableWidget.resizeRowsToContents()

		self.tableWidget.verticalHeader().hide()


	def insert(self):
		numColumns = self.tableWidget.columnCount()
		numRows = self.tableWidget.rowCount()

		data = [None]*numColumns
		string = "User(id, Name)..."
		string2 = "VALUES(%s, %s)..."
		string = self.tableName+"("
		string2 = "VALUES("

		for i in range(numColumns):
			string += self.columnsName[i] + ","
			string2 += "%s,"
			data[i] = self.tableWidget.item(numRows-1, i).data(0)

			if(data[i]=="None"):
				data[i] = None

		string = string[:len(string)-1] + ')'
		string2 = string2[:len(string2)-1] + ')'
		
		mycursor.execute("INSERT INTO "+string+string2, data)
		mydb.commit()

		mycursor.execute("SELECT * FROM "+str(self.tableName))
		rows = mycursor.fetchall()

		self.loadTableData(rows)

	def update(self):
		numColumns = self.tableWidget.columnCount()
		numRows = self.tableWidget.rowCount()

		data = [None]*(numColumns+1)
		string = "User SET"
		string2 = "VALUES(%s, %s)..."
		string = self.tableName+" SET "
		string2 = "VALUES("

		index = self.tableWidget.currentRow()
		
		for i in range(numColumns):
			string += self.columnsName[i] + " = %s,"
			data[i] = self.tableWidget.item(index, i).data(0)

			if(data[i]=="None"):
				data[i] = None

		data[numColumns] = data[0]

		string = string[:len(string)-1]
		string2 = " WHERE "+self.columnsName[0]+"=%s"

		mycursor.execute("UPDATE "+string+string2, data)
		mydb.commit()

		mycursor.execute("SELECT * FROM "+str(self.tableName))
		rows = mycursor.fetchall()

		self.loadTableData(rows)

	def delete(self):
		numColumns = self.tableWidget.columnCount()
		numRows = self.tableWidget.rowCount()

		string = "User"
		string2 = "Id = %s..."

		index = self.tableWidget.currentRow()

		data = self.tableWidget.item(index, 0).data(0)

		string = self.tableName
		string2 = " WHERE "+self.columnsName[0]+"=%s"

		mycursor.execute("DELETE FROM "+string+string2, (data, ))
		mydb.commit()

		mycursor.execute("SELECT * FROM "+str(self.tableName))
		rows = mycursor.fetchall()

		self.loadTableData(rows)

	def medicalHistory(self):
		self.tableName = "Med_History"
		index = self.tableWidget.currentRow()
		patient_id = self.tableWidget.item(index, 0).data(0)

		mycursor.execute("SELECT * FROM "+str(self.tableName)+" WHERE patient_id=%s", (patient_id, ))
		rows = mycursor.fetchall()

		self.loadTableData(rows)

	def appointment(self):
		self.tableName = "Appointment"
		index = self.tableWidget.currentRow()

		mycursor.execute("SELECT * FROM "+str(self.tableName))
		rows = mycursor.fetchall()

		self.loadTableData(rows)

		self.appoinWind = QMainWindow()
		appoinUi = appointment_ui()
		appoinUi.setupUi(self.appoinWind)
		appoinUi.pushButton.clicked.connect(partial(self.appoin_submit, appoinUi))
		self.appoinWind.show()

	def appoin_submit(self, appoinUi):
		doc_id = appoinUi.lineEdit.text()
		patient_id = appoinUi.lineEdit_2.text()

		mycursor.execute("SELECT COUNT(patient_id) FROM Appointment WHERE doctor_id=%s", (doc_id, ))
		havingPatients, = mycursor.fetchone()

		mycursor.execute("SELECT consult_capacity FROM Doctor WHERE doctor_id=%s", (doc_id, ))
		numPatients, = mycursor.fetchone()

		if(havingPatients+1 > numPatients):
			self.messagebox("Admin Message", "Sorry appointment not fixed, doctor is full")

		else:
			mycursor.execute("INSERT INTO Appointment VALUES(%s, %s)", (patient_id, doc_id))
			mydb.commit()

			self.tableName = "Appointment"
			index = self.tableWidget.currentRow()

			mycursor.execute("SELECT * FROM "+str(self.tableName))
			rows = mycursor.fetchall()

			self.loadTableData(rows)

			self.appoinWind.close()
			self.messagebox("Admin Message", "Appointment fixed successfully!")

	def emerAlert(self):
		currTime = datetime.now().strftime("%H:%M:%S")
		mycursor.execute("SELECT * FROM Doctor")
		records = mycursor.fetchall()
		rows = []

		c1 = datetime.strptime(currTime, '%H:%M:%S')

		for item in records:
			c2 = datetime.strptime(str(item[4]), '%H:%M:%S')
			if(c1 < c2):
				rows.append(item)
		
		self.loadTableData(rows)

		self.emerWind = QMainWindow()
		emerUi = emergency_ui()
		emerUi.setupUi(self.emerWind)
		emerUi.pushButton.clicked.connect(partial(self.emer_submit, emerUi))
		self.emerWind.show()


	def showBed(self):
		row=[];
		mycursor.execute("SELECT * FROM Bed_record where status='V'");
		records=mycursor.fetchall();
		for items in records:
			row.append(items);

		self.loadTableData(row);

	def payBill(self):
		self.payBillWind = QMainWindow()
		payBillUi = payBill_ui()
		payBillUi.setupUi(self.payBillWind)
		payBillUi.pushButton.clicked.connect(partial(self.payBill_submit, payBillUi))
		self.payBillWind.show()
	
	def payBill_submit(self, payBillUi):
		pat_id = payBillUi.lineEdit.text()
		print(pat_id);

		mycursor.execute("SELECT * FROM Bed_record where patient_id = %s",(pat_id,))
		records=mycursor.fetchone();
		print(records);

		ward_id=records[2];
		mycursor.execute("SELECT Ward_type FROM Wards where ward_id = %s",(ward_id,))
		ward_type=mycursor.fetchone();
		print(ward_type[0]);

		print(records[4]);
		temp1=str(records[4]);
		temp2=str(records[5]);
		strt_date=date(int(temp1[0:4]),int(temp1[5:7]),int(temp1[8:10]));
		end_date=date(int(temp2[0:4]),int(temp2[5:7]),int(temp2[8:10]));
		print(strt_date,end_date);
		diff=end_date-strt_date;
		print(diff.days);
		no_of_days=diff.days;

		if(ward_type[0]=='1'):
			bill=500*no_of_days;
		elif(ward_type[0]=='2'):
			bill=400*no_of_days;
		elif(ward_type[0]=='3'):
			bill=300*no_of_days;

		self.payBillWind.close()
		self.messagebox("Admin Message", "Please pay the bill of "+str(bill));

		mycursor.execute("UPDATE Bed_record set date_in=NULL, date_out=NULL, status='V', patient_id=NULL where patient_id=%s",(pat_id,))
		mydb.commit();

		self.tableName = "Bed_record"
		index = self.tableWidget.currentRow()

		mycursor.execute("SELECT * FROM "+str(self.tableName))
		rows = mycursor.fetchall()

		self.loadTableData(rows)


	def emer_submit(self, emerUi):
		doc_id = emerUi.lineEdit.text()
		msg = emerUi.textEdit.toPlainText()

		mycursor.execute("INSERT INTO Emergency_Alert VALUES(%s, %s)", (msg, doc_id))
		mydb.commit()

		self.emerWind.close()
		self.messagebox("Admin Message", "Emergency message sent successfully");
		
	def messagebox(self, title, message):
		w=QWidget()
		QMessageBox.information(w, title, message)
		w.show()

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainApp()
	window.show()
	sys.exit(app.exec_())