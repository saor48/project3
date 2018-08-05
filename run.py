"""to fix
Heroku - not resetttinf users,txt
Timeout- affecting chat input box =>
partial reload by div=jquery?
"""
"""to add
list of verbs, nouns
1. search phrase for verb
2, look for noun before and after for statements
"""
"""option
multi-thread searching

"""
import os
from flask import Flask, redirect, render_template, request, url_for
import csv

app = Flask(__name__)
phrases = []    
users = []      
chatters = 0    #current number of users online
lines = 0       #enumerate each chat line
previous = {}   #store previous message for each user
sourcelist = "data/wordlist.txt"
     # adapted from https://github.com/first20hours/google-10000-english
sourcelist2 = "data/google-10k-english.txt"  

def add_phrase(username, message, lines):
    phrases.append("{2}> {0}: {1}".format(username, message, lines))

def previousMessage(username):
    key = str(username)
    if key in previous.keys():
        message = previous[key]
    else:
        message = "xxx no previous message xxx"
    return message
    
def parse_phrases(words):
    corrected = ""
    """
    with open(sourcelist, "r") as word_list:
        reader = csv.reader(word_list, delimiter=',')
        """
    with open(sourcelist2, "r") as word_list:  
        filelist = word_list.read().splitlines()   
        for word in words:
            if word.lower() in filelist:
                corrected += " " + word
            else:
                word = '[' + word + ']'
                corrected += " " + word
    print("corrected-", corrected)
    return corrected
    
@app.route('/', methods=["GET","POST"])
def index():
    global chatters
    if request.method == "POST":
        chatters += 1
        if chatters == 1:
            #erase old users from file
            with open("data/users.txt", "w") as user_list:
                 user_list.close()
        with open("data/users.txt", "a") as user_list:
            user_list.writelines(request.form["username"] + "\n")
        return redirect(request.form["username"]) 
    return render_template("index.html")
 
@app.route('/<username>',  methods=["GET","POST"]) 
def username(username):
    global lines, previous
    name = username.title()
    with open("data/users.txt", "r") as user_list:  
        users = user_list.readlines()
    if request.method == "POST":
        message = request.form["message"]
        if str(message) != "":
            if str(message) != previousMessage(username):     #dont reload POST data
                previous[str(username)] = str(message)
                lines += 1
                words = message.split(' ')
                message = parse_phrases(words)
                add_phrase(username, message, lines)
            
    return render_template("chat.html", 
                username=name, chat_messages=phrases, users=users, chatters=chatters )
  
  
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)