from flask import Flask, render_template, request, jsonify
import datetime
import random

app = Flask(__name__) 
#app.debug = True
 
@app.route('/') 
def index():
    return render_template('index.html') 

if __name__ == '__main__':
    app.run()