from flask import Flask, request, url_for, render_template_string
import re

app=Flask(__name__)

@app.route('/', methods=('GET','POST'))
def index():
	if request.method=='POST':
		note=request.form['note']
		if sanitize(note):
			return render_template_string(note)
		else:
			return('Please provide some text')
	return '''
		<form method="POST">
			Note:<input type="text" name="note">
			<input type="submit" value="Submit">
		</form>
	'''

def sanitize(x):
	if "." in x:
		return False
	return True

if __name__=='__main__':
	app.run(host='0.0.0.0',port= 80,debug=True) 