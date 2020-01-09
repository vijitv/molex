###################################
#Author: Vatsal Nayak/ Vijit Vengsarkar
#Script Name: Printing_jobs_exception.py (Compare)
#Execution: python Printing_jobs_exception.py
#Motive: To compare the alternate parts ismatch b/w Zeppelin and Epicor
#Audit Trail:
#Date			Developer						Comment
#12/20/2019		Vijit Vengsarkar/Vatsal Nayak	First Release
####################################
import shutil
import sys
from PyQt5.QtWidgets import * #QApplication, QWidget, QInputDialog, QLineEdit, QLabel , QPushButton, QPlainTextEdit, QTextEdit 
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import datetime
import os


#Path Change----------------------------------------------------------------- The path changed here are used on line 124,125
script_folder_path = 'C://Users//vnayak//Desktop//Python Code//'      				#replace all the '\' in the path copied to '//' and add '//' at the end of the path
print_server_folder_path =  'L://xxxxx//requests//xxxxx//New folder//'		#replace all the '\' in the path copied to '//' and add '//' at the end of the path

#Function runs port clicking "WO Print"
def print_order():
	order_number = nameTextbox1.text()
	seq_number = int(nameTextbox3.text())
	copies = int(nameTextbox4.text())
	while True:
		if len(order_number) > 12:
			raise ValueError('Please enter a correct Order Number less than length 12') #error checking to limit the wrong Order number, will throw an error when the number entered is more than 10 digit excluding the '-'
			break
		elif seq_number > 100:
			raise ValueError('Please enter sequence number less than 100')  #error checking to limit the number of sequence to 100
			break
		elif copies > 100:
			raise ValueError('Please enter copies less than 100') #error checking to limit the number of copies to 100
			break
		else:
			final_doc_prep(order_number,seq_number,copies)
			break
	
	
	

# Function runs when clicking "Job Print" button 
# if the only Job print has to be done take values from the number of copies 
def print_job():   
	if nameTextbox2.text() and nameTextbox1.text():
		copies = int(nameTextbox3.text())
	elif nameTextbox2.text():
		copies = int(nameTextbox4.text())
	job_number = nameTextbox2.text()
	final_job_print(job_number,copies)

def final_job_print(job_number,copies):
	for i in range(0,copies):
		print("sn,job_number,"+job_number+',rev,top_serial_id,top_sn,top_part')
		with open("test.txt", "a") as myfile:
			myfile.write("sn,job_number,"+job_number+',rev,top_serial_id,top_sn,top_part\n')


def Clear():
	nameTextbox1.clear()
	nameTextbox2.clear()
	nameTextbox3.clear()
	nameTextbox4.clear()
	prompt = QMessageBox()
	#prompt.setStyleSheet("{font: 2pt Avenir Next}")
	prompt.about(window,"Message", "<font 	size = 2 >Ready for new print </font>")
	open('test.txt', 'w').close()
	print('sn,job_number,Number,rev,top_serial_id,top_sn,top_part------------------------------------')
	with open("test.txt", "a") as myfile:
		myfile.write('sn,job_number,Number,rev,top_serial_id,top_sn,top_part\n')
	
	




def final_doc_prep(order_number,seq_number,copies):
	while True:
		if '-' in order_number:
			break
		else:
			raise ValueError('Please Enter an order number with \'-\'')
			break
	
	for i in range(0,len(order_number)):
		if order_number[i] == '-':
			prefix = order_number[0:i]
			suffix = order_number[i+1:len(order_number)]			
	suffix_list=[]

	if suffix[-1] in ('F','f'):
		suffix_int = int(suffix[0:len(suffix)-1])

		for i in range(0,seq_number):            
			for j in range(0,copies):

				print("sn,work_order,"+prefix+'-'+format(suffix_int+i, "05")+'F'+',rev,top_serial_id,top_sn,top_part')
				with open("test.txt", "a") as myfile:
					myfile.write("sn,work_order,"+prefix+'-'+format(suffix_int+i, "05")+'F'+',rev,top_serial_id,top_sn,top_part\n')
	else:
		suffix_int = int(suffix[0:len(suffix)])

		for i in range(0,seq_number):
			for j in range(0,copies):
				print("sn,work_order,"+prefix+'-'+format(suffix_int+i, "05")+',rev,top_serial_id,top_sn,top_part')
				with open("test.txt", "a") as myfile:
					myfile.write("sn,work_order,"+prefix+'-'+format(suffix_int+i, "05")+',rev,top_serial_id,top_sn,top_part\n')




def Apply():
	if nameTextbox1.text()  and nameTextbox2.text():
		print_order()
		print_job()
		
	elif nameTextbox2.text():
		print_job()
	elif nameTextbox1.text():
		print_order()
	
	dt=str(datetime.datetime.now())
	date = dt[0:10]
	hours = dt[11:13]
	mins = dt[14:16]
	sec = dt[17:19]
	label = date+"_"+hours+mins+sec+".txt"
	os.rename(script_folder_path+'test.txt',script_folder_path+label)
	shutil.move(script_folder_path+label, print_server_folder_path+label)
	open('test.txt', 'w').close()
	print('sn,job_number,Number,rev,top_serial_id,top_sn,top_part------------------------------------')
	with open("test.txt", "a") as myfile:
		myfile.write('sn,job_number,Number,rev,top_serial_id,top_sn,top_part\n')
	prompt = QMessageBox()
	prompt.setStyleSheet("{font: 2pt Avenir Next}")
	prompt.about(window,"Message", "<font size = 2 >Printing Executed </font>")






open('test.txt', 'w').close()
print('sn,job_number,Number,rev,top_serial_id,top_sn,top_part------------------------------------')
with open("test.txt", "a") as myfile:
	myfile.write('sn,job_number,Number,rev,top_serial_id,top_sn,top_part\n')

#Developing the structure of the GUI
app=QApplication(sys.argv)
window=QWidget()
p = window.palette()
p.setColor(window.backgroundRole(), QtCore.Qt.lightGray)
window.setPalette(p)
window.setWindowTitle("Print GUI")
window.setGeometry(40,40,650,700)


#Setting Default font
#----------------------------------------------------------
window.setStyleSheet("QLabel {font: 20pt Avenir Next}")


validator = QIntValidator()

#input work order
Input_label1 = QLabel('Input Work Order Number:', parent = window)
Input_label1.move(50, 100+50+50)
nameTextbox1 = QLineEdit(parent=window)
nameTextbox1.setFixedWidth(350)
nameTextbox1.move(100-50,150+50+50)

#input Job Number 5
Input_label2 = QLabel('Input Job Number:', parent = window)
Input_label2.move(50, 200+50+50)
nameTextbox2 = QLineEdit(parent=window)
nameTextbox2.setFixedWidth(350)
nameTextbox2.setValidator(validator)				#Restricts the input to be exclusively integer
nameTextbox2.move(50,250+50+50)

#input seq 2
Input_label3 = QLabel('Input Sequence:', parent = window)
Input_label3.move(50, 300+50+50)
nameTextbox3 = QLineEdit(parent=window)
nameTextbox3.setFixedWidth(350)
nameTextbox3.setValidator(validator)			#Restricts the input to be exclusively integer
nameTextbox3.move(50,350+50+50)


#input copies 3
Input_label4 = QLabel('Input copies:', parent = window)
Input_label4.move(50, 400+50+50)
nameTextbox4 = QLineEdit(parent=window)
nameTextbox4.setFixedWidth(350)
nameTextbox4.setValidator(validator)				#Restricts the input to be exclusively integer
nameTextbox4.move(50,450+50+50)


#Button to Print/Apply 3
button1 = QPushButton("Print",parent=window)
button1.setStyleSheet("font-size: 20px;height: 48px;width: 120px;")
button1.move(450,500+25)
button1.clicked.connect(Apply)

#Button to Clear 4
button2 = QPushButton("Clear",parent=window)
button2.setStyleSheet("font-size: 20px;height: 48px;width: 120px;")
button2.move(450,400+25)
button2.clicked.connect(Clear)

#IMAGE
Image = QLabel(parent=window)
pixmap = QPixmap("Molex_Logo.png")
Image.setPixmap(pixmap)
	
window.show()
sys.exit(app.exec_())



