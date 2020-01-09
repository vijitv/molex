###################################
#Author: Vijit Vengsarkar/ Vatsal Nayak
#Script Name: compare_zep_epi.py (Compare)
#Execution: python compare_zep_epi.py
#Motive: To compare the alternate parts match b/w Zeppelin and Epicor a PostgreSQL database and a MySQL database respectively
#Audit Trail:
#Date			Developer						Comment
#12/20/2019		Vijit Vengsarkar	            First Release
####################################
import sys
import csv
import psycopg2
import pyodbc
import os
import smtplib
import email.message
import datetime
today = datetime.datetime.today()

##Function to deal with the connectivity of Zeppelin database and filtering zeppelin data
def zeppelin():
	server='xxxxx'
	database='xxxxx'
	username='xxxxx'
	password='xxxxx'
	port='5432'
	
	cnxn = psycopg2.connect(host="xxxxx",user="xxxxx",password="xxxxx",dbname="xxxxx");
	cursor = cnxn.cursor()
	query="select p.pn || '-' || trim(to_char(p.rev, '00')) as pcombo, string_agg( DISTINCT r.pn || '-' || trim(to_char(r.rev, '00'))  , ', ' order by r.pn || '-' || trim(to_char(r.rev, '00')) desc) as alts from parts p,parts r, boms b, parts a where b.assembly_id = a.id and b.contains_id = r.id and b.replaces_id = p.id and a.part_status_id != 3 and p.part_status_id != 3 and r.part_status_id != 3 group by p.pn, p.rev having  p.pn not like 'NPR%'  and (p.pn || '-' || trim(to_char(p.rev, '00'))  <> string_agg( DISTINCT r.pn || '-' || trim(to_char(r.rev, '00'))  , ', ' order by r.pn || '-' || trim(to_char(r.rev, '00')) desc)  ) order by pcombo"
	cursor.execute(query)
	with open("out_zeppelin.csv", "w", newline='') as csv_file:
		csv_writer = csv.writer(csv_file)
		csv_writer.writerow([i[0] for i in cursor.description])
		csv_writer.writerows(cursor)
	rows = cursor.fetchall()
	for row in rows:
		print(row, end='\n')
	
	zeppelin.lineList_zep = [line.rstrip('\n') for line in open('out_zeppelin.csv')] ##convert zeppelin file into a list
	zeppelin.lineList_zep = (zeppelin.lineList_zep[1:]) ##remove header
	zeppelin.split_zep_suf = [i.split(',', 1)[1] for i in zeppelin.lineList_zep] ##only alternates for zeppelin
	zeppelin.split_zep_pre = [i.split(',', 1)[0] for i in zeppelin.lineList_zep]##only main parts for zeppelin
	zeppelin.split_zep_suf = [i.split(',', 1)[0] for i in zeppelin.split_zep_suf] ## take only one value from alternate parts if many from zeppelin
	zeppelin.split_zep_suf = [item.replace("\"", "") for item in zeppelin.split_zep_suf]##remove the "

##Function to deal with the connectivity of Epicor database and filtering epicor data
def epicor():
	host = "xxxxx"
	database = "xxxxx"
	username = "xxxxx"
	password = "xxxxx"
	
	cs = 'DSN=%s;UID=%s;PWD=%s;DATABASE=%s;' % (host, username, password, database)
	cnxn = pyodbc.connect(cs)
	cursor = cnxn.cursor()
	
	cursor.execute('select Company, PartNum, SubPart, RecType, Comment_ as Comment from partsubs')
	with open("out_epicor.csv", "w", newline='') as csv_file:
		csv_writer = csv.writer(csv_file)
		csv_writer.writerow([i[0] for i in cursor.description])
		csv_writer.writerows(cursor)
		
	rows = cursor.fetchall()
	for row in rows:
		print(row, end='\n')
	
	epicor.lineList_epi = [line.rstrip('\n') for line in open('out_epicor.csv')] ##convert epicor file into a list
	epicor.lineList_epi = (epicor.lineList_epi[1:]) ##remove header
	epicor.split_epi_suf = [i.split(',', 3)[2] for i in epicor.lineList_epi] ##only alternates for epicor
	epicor.split_epi_pre = [i.split(',', 2)[1] for i in epicor.lineList_epi] ##only main parts for epicor

#Main function dealing with the logic of comparing and represening the new data
def main():
	sample_list = []
	for list_index_zep in range(0, len(zeppelin.split_zep_pre)):
		zeppelin.list_item_zep_pre = zeppelin.split_zep_pre[list_index_zep]
		zeppelin.list_item_zep_suf = zeppelin.split_zep_suf[list_index_zep]
		if zeppelin.list_item_zep_pre in epicor.split_epi_pre and zeppelin.list_item_zep_suf in epicor.split_epi_suf:
			continue
		elif zeppelin.list_item_zep_pre in epicor.split_epi_pre and zeppelin.list_item_zep_suf not in epicor.split_epi_suf:
			index_epi = epicor.split_epi_pre.index(zeppelin.list_item_zep_pre)
			print("Alternate part mismatch for Zeppelin part "+zeppelin.list_item_zep_pre+". Alternate part in Zeppelin: "+zeppelin.list_item_zep_suf+". Alternate part in Epicor:", epicor.split_epi_suf[index_epi], file=open("output.txt", "a"))
			sample_list.append(epicor.split_epi_suf[index_epi])
		else:
			print("Alternate part "+zeppelin.list_item_zep_suf+" is missing in Epicor", file=open("output.txt", "a"))
	for list_index_epi in range(0, len(epicor.split_epi_pre)):
		epicor.list_item_epi_pre = epicor.split_epi_pre[list_index_epi]
		epicor.list_item_epi_suf = epicor.split_epi_suf[list_index_epi]
		if epicor.list_item_epi_suf not in zeppelin.split_zep_suf and epicor.list_item_epi_suf not in sample_list:
			print("Extra alternate part "+epicor.list_item_epi_suf+" found in Epicor for Epicor main part:", epicor.split_epi_pre[list_index_epi], file=open("output.txt", "a"))
	os.remove('out_epicor.csv')
	os.remove('out_zeppelin.csv')

##Email function to set up parameters
def send_email(subject, msg):
	try:
		server = smtplib.SMTP('smtp.office365.com', 587)
		server.ehlo()
		server.starttls()
		ID = 'xxxxx'
		PASSWORD = 'xxxxx'
		email_reciever = 'xxxxx'
		server.login(ID, PASSWORD)
		message = 'Subject:{} \n\n {}'.format(subject, msg)
		server.sendmail(ID, email_reciever, message)
		os.remove('output.txt')
		print('Success')
	except Exception as e:
	   print(e) # Print any error messages to stdout
	finally:
		server.quit()

#Function calls		
zeppelin()
epicor()
main()

#Mailing logic
filename = r"output.txt"
with open(filename, "r") as filename:
    text = filename.read()
msg = email.message.Message()
msg.add_header('Content-Type', 'text/plain')
msg.set_payload(text)
subject = "Test report for Zeppelin and Epicor data mismatch for " + str(today.strftime("%m/%d/%y %H:%M:%S"))
send_email(subject, msg)