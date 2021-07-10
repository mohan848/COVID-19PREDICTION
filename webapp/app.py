from flask import Flask, render_template, request,jsonify,redirect, url_for, session,Response
from flask_mysqldb import MySQL

import MySQLdb.cursors
import re
from keras.models import load_model
import cv2
import numpy as np
import base64
from PIL import Image
from datetime import date
import io
import re
import string    
import random
from keras.models import load_model
import numpy as np 
import cv2                 
import numpy as np         
import os                  
from random import shuffle
import tensorflow as tf 
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import glob as gb
from tensorflow.keras.utils import to_categorical
import keras
from keras.layers import *
from keras.models import *
from keras.preprocessing import image
from keras.callbacks import EarlyStopping
from keras.callbacks import ModelCheckpoint
from keras.callbacks import LearningRateScheduler
from werkzeug.utils import secure_filename
import imageio
import base64
from fpdf import FPDF
import vonage
client = vonage.Client(key="a81c3814", secret="SB17VdubTUZ4nWL0")
sms = vonage.Sms(client)


app = Flask(__name__) 

app.secret_key = 'mohan'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'diagnosis'

# Intialize MySQL
mysql = MySQL(app)



model=tf.keras.models.load_model('model/model.h5')

label_dict={0:'Covid19 Positive', 1:'Normal',2:'Pneumonia'}

@app.route("/")
def index():
	return(render_template("index.html"))

@app.route("/test")
def test():
	return (render_template("test.html"))

@app.route("/userlogin")
def userlogin():
	return (render_template("userlogin.html"))

@app.route("/employeelogin")
def employeelogin():
	return (render_template("employeelogin.html"))

@app.route("/admindashboard")
def admindashboard():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT ID,name,gender,mobile_num FROM user_details where status="Y" ')
		pending=cursor.fetchall()
		cursor.execute('SELECT result,COUNT(*) FROM test_results GROUP BY result')
		data1 = cursor.fetchall()
		#print(data1)
		#print(type(data1))
		if len(data1)==3:
			label1=data1[0].get('result')
			label2=data1[1].get('result')
			label3=data1[2].get('result')
			count1=data1[0].get('COUNT(*)')
			count2=data1[1].get('COUNT(*)')
			count3=data1[2].get('COUNT(*)')
			data={'Result': 'Count',label1: count1,label2: count2,label3: count3}
			print(data)
		cursor.execute('SELECT COUNT(*) FROM user_details')
		enrolled_count = cursor.fetchone()
		cursor.execute('SELECT COUNT(*) FROM user_details where status="Y" ')
		pending_count=cursor.fetchone()
		cursor.execute('SELECT COUNT(*) FROM user_details where status="D" ')
		completed_count=cursor.fetchone()
		return render_template('admindashboard.html',pending=pending,data=data,pending_count=pending_count,completed_count=completed_count,enrolled_count=enrolled_count)

@app.route("/userdashboard")
def userdashboard():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT ID,result FROM test_results where ID=%s ',(session['ID'],))
		tests=cursor.fetchall()
		return (render_template("userdashboard.html",tests=tests))




@app.route("/addpatient")
def addpatient():
	return (render_template("addpatient.html"))



@app.route("/addpatient/",methods=['GET', 'POST'])
def addpatientintodatabase():
	patmsg=''

	if request.method == 'POST' and 'name' in request.form and 'gender' in request.form and 'mbnum' in request.form and 'age' in request.form:
		name=request.form['name']
		gender=request.form['gender']
		mobilenum=request.form['mbnum']
		age=request.form['age']
		email=request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		S = 8
		genpassword = str(''.join(random.choices(string.ascii_uppercase + string.digits, k = S)))  

		if not name.isalpha():
			patmsg = 'Invalid Name!'
		elif not mobilenum.isdigit():
			patmsg = 'Invalid Mobile Number!'
		elif not len(mobilenum)==10:
			patmsg = 'Invalid Mobile Number!'
		else:
			cursor.execute('INSERT INTO user_details VALUES (NULL, %s, %s, %s,%s,%s,%s,"Y")', (email, name, gender,age,mobilenum,genpassword))
			mysql.connection.commit()

			cursor.execute('select ID,password from user_details ORDER BY ID DESC LIMIT 1')
			logindata = cursor.fetchone()
			#print(logindata)
			patmsg = 'Successfully Added!'+'\n'+'ID: '+str(logindata.get('ID'))+' Pwd: '+genpassword

	elif request.method == 'POST':
		patmsg = 'Please fill out the form!'
	return render_template('addpatient.html', msg=patmsg)

@app.route("/updateprofile",methods=['GET', 'POST'])
def update_profile():
	patmsg=''
	if request.method == 'POST' and 'ppass' in request.form:
		id=request.form['pid']
		ppass= request.form['ppass']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('UPDATE user_details SET password=%s where ID= %s',(ppass,id,))
		mysql.connection.commit()

	return redirect("http://127.0.0.1:5000/userprofile")


@app.route("/employeelogin/",methods=['GET', 'POST'])
def login():
	msg=''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username=request.form['username']
		password = request.form['password']
		cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM employee_details WHERE username = %s AND password = %s', (username, password,))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			#session['id'] = account['id']
			session['username'] = account['username']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT ID,name,gender,mobile_num FROM user_details where status="Y" ')
			pending=cursor.fetchall()
			cursor.execute('SELECT result,COUNT(*) FROM test_results GROUP BY result')
			data1 = cursor.fetchall()
			#print(data1)
			#print(type(data1))
			if len(data1)==3:
				label1=data1[0].get('result')
				label2=data1[1].get('result')
				label3=data1[2].get('result')
				count1=data1[0].get('COUNT(*)')
				count2=data1[1].get('COUNT(*)')
				count3=data1[2].get('COUNT(*)')
				data={'Result': 'Count',label1: count1,label2: count2,label3: count3}
			cursor.execute('SELECT COUNT(*) FROM user_details')
			enrolled_count = cursor.fetchone()
			#print(enrolled_count)
			#print(type(enrolled_count))
			cursor.execute('SELECT COUNT(*) FROM user_details where status="Y" ')
			pending_count=cursor.fetchone()
			#print(pending_count)
			cursor.execute('SELECT COUNT(*) FROM user_details where status="D" ')
			completed_count=cursor.fetchone()
			#print(completed_count)
			return render_template('admindashboard.html',pending=pending,data=data,pending_count=pending_count,completed_count=completed_count,enrolled_count=enrolled_count)
		else:
			msg = 'Incorrect username/password!'
	return render_template('employeelogin.html', msg=msg)

@app.route('/employeelogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('ID', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/userlogin/logout')
def userlogout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('userloginauth'))

@app.route('/admindashboard/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee_details WHERE username = %s', (session['username'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('adminprofile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/uploadresults')
def uploadresults():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT ID,name FROM user_details where status="Y" ')
		pendinglist=cursor.fetchall()
		return render_template('test.html', pendinglist=pendinglist)


@app.route("/predict", methods=["POST"])
def predict():
	#print('HERE')
	message = request.get_json(force=True)
	encoded = message['image']
	decoded = base64.b64decode(encoded)
	dataBytesIO=io.BytesIO(decoded)
	dataBytesIO.seek(0)
	image1 = Image.open(dataBytesIO)
	#print(image1.size)
	image1 = image1.resize((400,400))
	#print(image1.size)
	np_img = np.array(image1)
	#print(np_img.shape)
	covid_img_array = np.expand_dims(np_img, axis=0)
	covid_img_array.shape
	prediction=model.predict(covid_img_array)
	a=np.argmax(prediction, axis =1)[0]

	accuracy=float(np.max(prediction,axis=1)[0])

	print(a)
	#print(accuracy)


	#prediction = model.predict()
	#result=np.argmax(prediction,axis=1)

	label=label_dict[a]
	print(label)

	#print(prediction,result,label)
	response = {'prediction': {'result': label}}

	return jsonify(response)

@app.route('/userprofile')
def userprofile():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user_details WHERE ID = %s', (session['ID'],))
		account = cursor.fetchone()
		return render_template('userprofile.html', account=account)

@app.route("/analytics")
def analytics():
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute('SELECT result,COUNT(*) FROM test_results GROUP BY result')
	data1 = cursor.fetchall()
	print(data1)
	print(type(data1))
	

	if len(data1)==3:
		label1=data1[0].get('result')
		label2=data1[1].get('result')
		label3=data1[2].get('result')
		count1=data1[0].get('COUNT(*)')
		count2=data1[1].get('COUNT(*)')
		count3=data1[2].get('COUNT(*)')
		data={'Result': 'Count',label1: count1,label2: count2,label3: count3}
	return render_template('admindashboard.html',data=data)



@app.route('/upload',methods=['GET','POST'])
def upload():
	print('here')
	status=''
	if request.method == 'POST' and 'pid' in request.form and 'myText' in request.form:
		#result=request.form['testresult']
		ID=request.form['pid']
		print(ID)
		result=request.form['myText']
		print(ID,result)
		
		#pic=request.files['pic']
		#print(pic)
		#pic.read
		#file = base64.b64encode(pic)
		#file=io.BytesIO(file)


		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor1= mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('INSERT INTO test_results VALUES (%s, %s)', (ID, result,))
		
		cursor.execute('UPDATE user_details SET status="D" where ID= %s',(ID,))

		cursor1.execute('SELECT * from user_details where ID=%s',(ID,))
		data1 = cursor1.fetchall()
		print(data1)
		name= data1[0].get('name')
		#contact=data1[0].get('mobile_num')
		#contactno="91"+contact
		#print(contactno)

		responseData = sms.send_message(
   		 {
        	"from": "M & D Diagnostics",
        	"to": "916379462299",
        	"text":  "M&D Diagnostis, "+"Hello "+name+", COVID-19 Detection using Chest X-Rays test result: "+result+". You can download test report here by clicking the link below.",
   		 }
		)
		if responseData["messages"][0]["status"] == "0":
			print("Message sent successfully.")
		else:
			print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

		mysql.connection.commit()
		status = 'Successfully Added!'
	return redirect("http://127.0.0.1:5000/uploadresults")

@app.route("/userlogin/",methods=['GET', 'POST'])
def userloginauth():
	msg=''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username=request.form['username']
		password = request.form['password']
		cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user_details WHERE ID = %s AND password = %s', (username, password,))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			#session['id'] = account['id']
			session['ID'] = account['ID']
			pid=session['ID']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

			cursor.execute('SELECT ID,result FROM test_results where ID=%s ',(pid,))
			tests=cursor.fetchall()
			#cursor.execute('SELECT ID,name,gender,mobile_num FROM user_details where status="Y" ')
			#pending=cursor.fetchall()
			return render_template('userdashboard.html',tests=tests)
		else:
			msg = 'Incorrect username/password!'
	return render_template('userlogin.html', msg=msg)


@app.route('/download/report/pdf')
def download_report():
	cursor = None
	try:
		print("pdf")
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT ID,result FROM test_results where ID=%s ',(session['ID'],))
		cursor1.execute('SELECT * FROM user_details where ID=%s ',(session['ID'],))		
		result = cursor.fetchone()
		result1 = cursor1.fetchone()
		
		pdf = FPDF()
		pdf.add_page()
		
		page_width = pdf.w - 2 * pdf.l_margin
		
		pdf.set_font('Times','B',16) 
		pdf.cell(page_width, 0.0, 'TEST REPORT', align='C')
		pdf.ln(10)

		pdf.cell(71 ,5,'M&D Diagnostics',0,0)
		pdf.cell(59 ,5,'',0,0)
		pdf.cell(59 ,5,'Patient Details',0,1)

		pdf.set_font('Courier', '', 14)

		pdf.cell(130 ,5,'Near VIT',0,0)
		pdf.cell(25 ,5,'ID:',0,0)
		pdf.cell(34 ,5,str(result['ID']),0,1)

		today = date.today()
		

		pdf.cell(130 ,5,'Chennai,600127',0,0)
		pdf.cell(25 ,5,'Name:',0,0)
		pdf.cell(34 ,5,str(result1['name']),0,1)
		

		pdf.cell(130 ,5,'Contact us : 1234567890',0,0)
		pdf.cell(25 ,5,'Age:',0,0)
		pdf.cell(34 ,5,str(result1['age']),0,1)

		pdf.cell(130 ,5,'Date: '+str(today),0,0)
		pdf.cell(25 ,5,'Gender:',0,0)
		pdf.cell(34 ,5,str(result1['gender']),0,1)
		data=[['TEST NAME','RESULT'],['COVID19 Detection using X-RAYS',result['result']]]
		
		col_width = page_width/3
		
		pdf.ln(8)
		th = pdf.font_size
		
		pdf.cell(110,6,'TEST NAME',1,0,'C')
		pdf.cell(70 ,6,'RESULT',1,1,'C')
		pdf.cell(110,6, 'COVID19 DETECTION USING CHEST X-RAYS',1,0)
		pdf.cell(70,6, result['result'],1,0,'C')

		#pdf.ln(3)
		#pdf.cell(180,6,'*Note: Above test report is generated by feeding your x ray to the AI machine',0,1)
		#pdf.cell(180,6,'and the results will be uploaded by diagnostics lab administrator.In case if any discrepancies contact diagnostics lab immediately.',0,0)
		#pdf.set_font('Times','',10.0) 
		#pdf.cell(page_width, 0.0, '* END OF REPORT *', align='C')
		
		return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=test_report.pdf'})
	except Exception as e:
		print(e)
	finally:
		cursor.close()
	

app.run(debug=True)

