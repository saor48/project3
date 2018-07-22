import os
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "<h4>some html</h4>"
    
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)