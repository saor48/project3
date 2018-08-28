"""to fix
Heroku - not reseting users.txt -----
chatters subtract   done but test
"""
"""to add
0.list of verbs, nouns
1. search phrase for verbs -done basic
2. second form input  -output to chat, how?
"""
"""option
asyncio - py3.5 modules not available in c9-py3.4
"""
import os, asyncio, time
from flask import Flask, redirect, render_template, request, url_for, flash
import csv, json
import structure
#use a new thread for json file write
from threading import Thread
import athread

app = Flask(__name__)
app.secret_key = os.urandom(24)
TEMPLATES_AUTO_RELOAD = False
PYTHONASYNCIODEBUG = 1

#newTHREAD = False
maxUSERS = 3
error_message = ""
phrases = []    # chat messages
userlog = {}      # current users online 
jsondict = {}   # chat message as json
chatters = 0    #current number of users online
line = 0       #enumerate each chat line
previous = {}   #store previous message for each user
score = {}      #hold current score for all users
leaderboard = [] #sorted list by top scorer
user_score = 0  # for this username
sourcelist = "data/wordlist.txt"
     # adapted from https://github.com/first20hours/google-10000-english
sourcelist2 = "data/8K-english.txt"  

# ---------------6-Functions-----------------------------------------#
#  add_phrase(username, corrected, line) -- append to list(phrases) + create json string
# new_thread(jsondict, chatline): --------- start new thread for below:
    # athread.json_phrases(jsondict, chatline)---append new message to json file
# previous_message(username) -------------- check if user submit button x2
# calc_score(corrected, username)---------- score each word then total
# calc_leaderboard(username, my_score) ---- reorder leaderboard
# parse_phrases(words)--------------------- check each word in message

def add_phrase(username, corrected, line):
    global jsondict
    jphrase = {}
    message = corrected[0]
    if corrected[2]:
        print("its a question!!!!!!!")
    chatline = "{2}> {0}: {1}".format(username, message, line)
    phrases.append(chatline)
    jphrase['line'] = str(line)
    jphrase['user'] = str(username)
    jphrase['message'] = str(message)
    jsondict[str(line)] = str(jphrase)
    new_thread(jsondict, chatline)

def new_thread(jsondict, chatline):
    timer = time.time()
    print('start new thread', timer)
    new_loop = asyncio.new_event_loop()
    t = Thread(target=athread.start_loop, args=(new_loop,))
    t.start()
    new_loop.call_soon_threadsafe(athread.json_phrases, jsondict, chatline)
    print('after loop call, delay=', time.time() - timer)
    new_loop.call_soon_threadsafe(athread.whois_online, userlog)
    print('2nd loop call, delay=', time.time() - timer)
    
def previous_message(username):
    key = str(username)
    if key in previous.keys():
        message = previous[key]
    else:
        message = "xxx no previous message xxx"
    return message

def calc_score(corrected, username):
    global score, leaderboard
    my_score = corrected[1]
    if str(username) in score:
        score[str(username)] += my_score
    else:
        score[str(username)] = my_score
    my_score = score[str(username)]
    calc_leaderboard(username, my_score)
    return my_score
    
def calc_leaderboard(username, my_score):
    global leaderboard
    if str(username) not in leaderboard:
        leaderboard.append(str(username))
    pos = leaderboard.index(str(username))
    for k, v in score.items():
        if my_score > score[str(k)]:
            kpos = leaderboard.index(str(k))
            if pos > kpos:
                leaderboard.remove(str(username))
                leaderboard.insert(kpos,str(username))
                
def parse_phrases(words):
    good=0
    bad=0
    corrected = ""
    question = False
    """
    with open(sourcelist, "r") as word_list:
        reader = csv.reader(word_list, delimiter=',')
        """
    with open(sourcelist2, "r") as word_list:  
        filelist = word_list.read().splitlines()   
        for word in words:
            if word == words[-1]:
                if word[-1] == '?':
                    word = word[:-1]
                    question = True
            if word.lower() in filelist:
                corrected += " " + word
                good += 1
            else:
                word = '[' + word + ']'
                corrected += " " + word
                bad += 1
    if question:
        corrected += '?'
    print("corrected-", corrected)
    score = good - bad
    return (corrected, score, question)
    
# ---------------4-VIEWS-----------------------------------------#
# '/'                       enter username then redirects to /username
# '/<username>'             main user chat page
# '/chat/messages'          updates each user with new messages
# '/chat/structure'         form to allow user to analyse any message line

# user sign in page
@app.route('/', methods=["GET","POST"])
def index():
    global chatters, error_message
    if request.method == "POST":
        chatters += 1
        if chatters == 1:
            #erase old users from file
            with open("data/users.txt", "w") as user_list:
                 user_list.close()
            #erase old messages from file
            with open("data/chatlines.txt", "w") as list:
                 list.close()
        if chatters <= maxUSERS: 
            timer = str(time.time())
            with open("data/users.txt", "a") as user_list:
                user_list.writelines(request.form["username"] + "\n")
            return redirect(request.form["username"]) 
        else:
            error_message = "Max Users exceeded - No Access"
            flash("Max Users exceeded - Access Denied")
            chatters -= 1
    return render_template("index.html", error=error_message)

# user chat page, handles all form inputs
@app.route('/<username>',  methods=["GET","POST"]) 
def username(username):
    global line, previous, score, user_score
    question = False
    name = username.title()
    with open("data/users.txt", "r") as user_list:
        users = user_list.readlines()
        print("users-", users)
        
    if request.method == "POST":
        # request for structure
        if not request.form["message"]:
            cc = request.form["cc"]
            line = int(request.form["line"])
            sq = request.form["sq"]
            message = ""
            print("cc--", cc,line,sq)
            structure.main(str(line))
        else:
            message = request.form["message"]
        # new messsage
        if str(message) != "":
            if str(message) != previous_message(username):     #dont reload POST data
                previous[str(username)] = str(message)
                line += 1
                words = message.split(' ')
                corrected = parse_phrases(words)
                add_phrase(username, corrected, line)
                user_score = calc_score(corrected, username)
  
    return render_template("chat.html", 
                username=name, chat_messages=phrases, users=users, 
                chatters=chatters, my_score=user_score, 
                score=score, leaderboard=leaderboard)

# update chat messages very 5 secs
@app.route('/chat/messages', methods=["GET","POST"])  
def messages(): 
    global userlog
    if request.method == "GET":
        user = request.args["user"]
        timer = time.time()
        userlog[user] = timer    #timestamp user for later check if still online
                  
    return render_template("messages.html", chat_messages=phrases,
                score=score, leaderboard=leaderboard)

# provide html to analyse phrase
@app.route('/chat/structure', methods=["GET","POST"])  
def struct(): 
    # "w3-include-html"
    return render_template("structure.html")
  
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
