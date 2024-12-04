from flask import Flask, request, url_for, render_template_string
import re

app=Flask(__name__)

@app.route('/', methods=('GET','POST'))
def index():
	try:
		if request.method=='POST':
			note=request.form['note']
			if sanitize(note):
				return render_template_string(note)
			else:
				return('Please provide valid text')
		return '''
			<form method="POST">
				Note:<input type="text" name="note">
				<input type="submit" value="Submit">
			</form>
		'''
	except:
		return ('Please provide valid text')

def sanitize(x):
	if "." in x:
		return False
	return True

if __name__=='__main__':
	app.run(host='0.0.0.0',port= 5000,debug=True) 
