import os
from flask import Flask, redirect

app = Flask(__name__)
phrases = []

def add_phrase(username, message):
    phrases.append("{0}: {1}".format(username, message))
    
def get_phrases():
    return "<br>".join(phrases)
    
@app.route('/')
def index():
    return "<h4><i>to send a message</i> : /your-name/message</h4>"
 
@app.route('/<username>') 
def username(username):
    username = username.title()
    return "<h4>Hi {0} </h4>".format(username) + get_phrases()
    
@app.route('/<username>/<message>') 
def message(username, message):
    add_phrase(username, message)
    return redirect(username)
    
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)