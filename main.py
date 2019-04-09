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
	password="yogislife",
	database="HMS"
)

mycursor = mydb.cursor()

ui,_ = loadUiType('main.ui')

class MainApp(QMainWindow, ui):
	def __init__(self):
		QMainWindow.__init__(self)
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

	def receptionist(self):
		self.prevIndex = self.stackedWidget.currentIndex()
		self.stackedWidget.setCurrentIndex(2);
		self.currIndex = self.stackedWidget.currentIndex()

	def infraAdmin(self):
		self.prevIndex = self.stackedWidget.currentIndex()
		self.stackedWidget.setCurrentIndex(3);
		self.currIndex = self.stackedWidget.currentIndex()

	def financeAdmin(self):
		self.prevIndex = self.stackedWidget.currentIndex()
		self.stackedWidget.setCurrentIndex(4);
		self.currIndex = self.stackedWidget.currentIndex()

	def backBtn(self):
		prevIndex = self.prevIndex
		self.prevIndex = self.stackedWidget.currentIndex()
		self.stackedWidget.setCurrentIndex(prevIndex);
		self.currIndex = self.stackedWidget.currentIndex()

	def nextBtn(self):
		self.prevIndex = self.stackedWidget.currentIndex()
		self.stackedWidget.setCurrentIndex(self.currIndex + 1);
		self.currIndex = self.stackedWidget.currentIndex()

	def showTable(self):
		_translate = QCoreApplication.translate
		radios = [[1,8,9], [2,10,11,12,13], [3,14,15]]

		for i in range(len(radios[self.currIndex - 2])):
			selected_radio = self.findChild(QRadioButton, "radioButton_"+str(radios[self.currIndex - 2][i]))
			if selected_radio.isChecked():
				self.tableName = selected_radio.text()
				mycursor.execute("SELECT * FROM "+str(self.tableName))
				rows = mycursor.fetchall()
				self.loadTableData(rows)
				break

		if(self.tableName == "Patient"):
			if(hasattr(self, 'pushButton_11')):
				self.pushButton_11.deleteLater()
			if(hasattr(self, 'pushButton_12')):
				self.pushButton_12.deleteLater()

			self.pushButton_11 = QPushButton(self.page_5)
			self.pushButton_11.setGeometry(QRect(270, 380, 141, 40))
			self.pushButton_11.setObjectName("pushButton_11")
			self.pushButton_11.setText(_translate("MainWindow", "Medical History"))
			self.pushButton_11.clicked.connect(self.medicalHistory)

		elif(self.tableName == "Doctor"):
			if(hasattr(self, 'pushButton_11')):
				self.pushButton_11.deleteLater()
			if(hasattr(self, 'pushButton_12')):
				self.pushButton_12.deleteLater()

			self.pushButton_11 = QPushButton(self.page_5)
			self.pushButton_11.setGeometry(QRect(210, 380, 111, 40))
			self.pushButton_11.setObjectName("pushButton_11")
			self.pushButton_12 = QPushButton(self.page_5)
			self.pushButton_12.setGeometry(QRect(340, 380, 131, 40))
			self.pushButton_12.setObjectName("pushButton_12")
			self.pushButton_11.setText(_translate("MainWindow", "Appointment"))
			self.pushButton_12.setText(_translate("MainWindow", "Emergency Alert"))

			self.pushButton_11.clicked.connect(self.appointment)
			self.pushButton_12.clicked.connect(self.emerAlert)
        
		self.prevIndex = self.stackedWidget.currentIndex()
		self.stackedWidget.setCurrentIndex(5)
		self.currIndex = self.stackedWidget.currentIndex()

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
		print("appo")

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