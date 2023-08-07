from flask import Flask, render_template, request, jsonify
from encode import encode, generate_key
import webbrowser
import json
import sys
import os

if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=os.path.join(base_dir, 'templates'), static_folder=os.path.join(base_dir, 'static'))

@app.route('/')
def index():
    return render_template('signin.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Check with JSON file
    with open('users.json', 'r') as f:
        users = json.load(f)
    
    if users.get(username) == password:
        return render_template('license.html')
    else:
        return "Invalid username or password", 401

@app.route('/generate_license', methods=['POST'])
def generate_license():
    date = request.form.get('date')
    secret_key = generate_key()
    license_key = encode(date, secret_key)
    return jsonify({"license": license_key})

@app.route('/sw.js')
def service_worker():
    return app.send_static_file('sw.js')

@app.route('/manifest.json')
def manifest_json():
    return app.send_static_file('manifest.json')

if __name__ == '__main__':
    if not os.environ.get('WERKZEUG_RUN_MAIN'):
        webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=False)
