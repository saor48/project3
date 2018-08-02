import os
from flask import Flask, redirect, render_template, request
import csv

app = Flask(__name__)
phrases = []    
users = []      
chatters = 0    #current number of users online
lines = 0       #enumerate each chat line
sourcelist = "data/wordlist.txt"
     # from https://github.com/first20hours/google-10000-english
sourcelist2 = "data/google-10000-english.txt"  

def add_phrase(username, message, lines):
    phrases.append("{2}> {0}: {1}".format(username, message, lines))
    
def split_message(message):
    words = message.split(' ')
    return words

def parse_phrases(phrase, words):
    corrected = ""
    """
    with open(sourcelist, "r") as word_list:
        reader = csv.reader(word_list, delimiter=',')
        """
    with open(sourcelist2, "r") as word_list:  
        filelist = word_list.read().splitlines()   
        for word in words:
            if word in filelist:
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
    username = username.title()
    with open("data/users.txt", "r") as user_list:  
        users = user_list.readlines()
    if request.method == "POST":
        message = request.form["message"]
        global lines
        lines += 1
        words = split_message(message)
        message = parse_phrases(message, words)
        add_phrase(username, message, lines)
    return render_template("chat.html", 
                username=username, chat_messages=phrases, users=users, chatters=chatters )
  
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)