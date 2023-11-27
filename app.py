from flask import Flask, render_template, request, session, jsonify
from uuid import uuid4
from os import urandom
import webbrowser

from src import generate_galaxy

app = Flask(__name__, template_folder='./html')
app.secret_key = urandom(16) # 16 byte random key for each new start

galaxies = { 'empty': [] }

@app.get('/')
def index():
    return render_template('index.html')


@app.get('/galaxy')
@app.get('/galaxy/<option>')
def galaxy(option=None):
    
    key = session.get('key')
    if key and not galaxies.get(key):
        session['key'] = uuid4() # galaxy doesn't exist for that session anymore
    
    if option == 'create':
        
        try:
            n = int(request.args.get('n', '10000'))
        except ValueError:
            n = 10000
        
        try:
            d = int(request.args.get('d', '100'))
        except ValueError:
            d = 0.5

        try:
            phi = float(request.args.get('phi', '0.5'))
        except ValueError:
            phi = 0.5

        try:
            galaxies[key] = generate_galaxy(n, d, phi)
        except Exception as error:
            print(error)
            return jsonify({"error": error.__dict__}), 500
    
    return galaxies.get(key, [])


if __name__ == "__main__":
    webbrowser.open_new_tab('http://127.0.0.1:3333')
    app.run(port=3333, debug=True)