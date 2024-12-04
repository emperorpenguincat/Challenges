from flask import Flask, request, render_template_string
import re
import unicodedata

app = Flask(__name__)

blacklisted = [r"\(", r"\)"]

@app.route('/', methods=('GET', 'POST'))
def index():
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

def sanitize(input_text):
    for pattern in blacklisted:
        if re.search(pattern, input_text):
            return False
    return True

def normalize_input(input_text):
    return unicodedata.normalize('NFKC', input_text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
