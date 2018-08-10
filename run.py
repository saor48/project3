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
import csv, json

app = Flask(__name__)
TEMPLATES_AUTO_RELOAD = False

phrases = []    
users = []  
jsondict = {}
chatters = 0    #current number of users online
line = 0       #enumerate each chat line
previous = {}   #store previous message for each user
sourcelist = "data/wordlist.txt"
     # adapted from https://github.com/first20hours/google-10000-english
sourcelist2 = "data/google-10k-english.txt"  

def add_phrase(username, message, line):
    global jsondict
    chatline = "{2}> {0}: {1}".format(username, message, line)
    phrases.append(chatline)
    jsondict[str(line)] = str(chatline)
    json_phrases(jsondict, chatline)

def json_phrases(jsondict, chatline):
    with open("data/chatlines.txt", "a") as chat:
            chat.writelines(str(chatline) + "\n")
    with open("data/chatlines.json", "w") as chatlines:
            json.dump(jsondict, chatlines)
    with open("data/chatlines.json", "r") as jlines:
            jsonlines = json.load(jlines)
    print ("json-", jsonlines)
    
def previous_message(username):
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
            #erase old messages from file
            with open("data/chatlines.txt", "w") as list:
                 list.close()
        with open("data/users.txt", "a") as user_list:
            user_list.writelines(request.form["username"] + "\n")
        return redirect(request.form["username"]) 
    return render_template("index.html", chat_messages=phrases)
 
@app.route('/<username>',  methods=["GET","POST"]) 
def username(username):
    global line, previous
    name = username.title()
    with open("data/users.txt", "r") as user_list:  
        users = user_list.readlines()
    if request.method == "POST":
        message = request.form["message"]
        if str(message) != "":
            if str(message) != previous_message(username):     #dont reload POST data
                previous[str(username)] = str(message)
                line += 1
                words = message.split(' ')
                message = parse_phrases(words)
                add_phrase(username, message, line)
            
    return render_template("chat.html", 
                username=name, chat_messages=phrases, users=users, chatters=chatters )

@app.route('/chat/messages', methods=["GET","POST"])  
def messages(): 
  return render_template("messages.html", chat_messages=phrases)
  
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)