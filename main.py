from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

from datetime import timedelta
from datetime import datetime

import sys

import mysql.connector

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="1234",
	database="HMS"
)

mycursor = mydb.cursor()

ui,_ = loadUiType('main.ui')
emergency_ui,_ = loadUiType('emergency.ui')

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

		if(self.tableName == "Patient"):
			if(hasattr(self, 'extraBtn1')):
				self.extraBtn1.deleteLater()
			if(hasattr(self, 'extraBtn2')):
				self.extraBtn2.deleteLater()

			self.extraBtn1 = QPushButton(self.page_5)
			self.extraBtn1.setGeometry(QRect(270, 380, 141, 40))
			self.extraBtn1.setObjectName("extraBtn1")
			self.extraBtn1.setText(_translate("MainWindow", "Medical History"))
			self.extraBtn1.clicked.connect(self.medicalHistory)

		elif(self.tableName == "Doctor"):
			if(hasattr(self, 'extraBtn1')):
				self.extraBtn1.deleteLater()
			if(hasattr(self, 'extraBtn2')):
				self.extraBtn2.deleteLater()

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
		print(type(data[0]))
		
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
		print("appointment btn clicked")

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

		emerUi.pushButton.clicked.connect(self.medicalHistory)

		self.emerWind.show()

# class reqWindow(QMainWindow, req):
# 	def __init__(self, objd):
# 		super(reqWindow, self).__init__(objd)
# 		self.setupUi(self)

# 		self.pushButton.clicked.connect(self.submit)

# 	def submit(self):
# 		user_id = self.lineEdit.text()
# 		book_id = self.lineEdit_2.text()

# 		if(fns.req_book(user_id, book_id) == False or fns.borrow_allowed(user_id) == False):
# 			self.messagebox("Admin Message","Sorry Book Can't Be Issued");
# 			print(fns.req_book_queue)

# 		else:
# 			mycursor.execute("UPDATE Book SET User_id = %s, IssueDate = %s, ReturnDate = %s WHERE Id = %s", (user_id, fns.date_today, None, book_id))
# 			mydb.commit()

# 		self.close()
		
# 	def messagebox(self, title, message):
# 		w=QWidget()
# 		QMessageBox.information(w, title, message)
# 		w.show()

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainApp()
	window.show()
	sys.exit(app.exec_())