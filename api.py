import flask
from flask_cors import CORS
from flask import request
import subprocess

app = flask.Flask(__name__)
CORS(app)

@app.route('/file', methods=['POST'])
def file():
    file = request.data.decode('utf-8')
    if file:
        with open('modified_sms_v2.xml', 'w') as f:
            f.write(file)
        list_of_subprocesses = [
            "/usr/bin/env sh prepare_me.sh",
            "/usr/bin/env python3 Categorizer.py",
            "/usr/bin/env python3 Cleaner.py",
            "/usr/bin/env python3 Db_saver.py"
        ]

        for subprocess_command in list_of_subprocesses:
            print(subprocess_command)
            subprocess.run(subprocess_command, shell=True)
        print("Done")
    
    else:
        print("Upload A file")

if __name__ == '__main__':
    app.run(debug=True, port=8000)
