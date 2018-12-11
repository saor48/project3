"""to fix
1. clean up form handling
"""
"""to add
0.list of verbs, nouns
1. list of test phrases
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
userlog = {}    # current users online 
jsondict = {}   # chat message as json
chatters = 0    #current number of users online
line = 0        #enumerate each chat line
previous = {}   #store previous message for each user
score = {}      #hold current score for all users
leaderboard = [] #sorted list by top scorer
user_score = 0  # for this username
     # adapted from https://github.com/first20hours/google-10000-english
sourcelist = "data/8K-english.txt"  

# ---------------7-Functions-----------------------------------------#
# add_phrase(username, corrected, line) --- append to list(phrases) + create json string
# new_thread(jsondict, chatline): --------- start new thread for below:
    # athread.json_phrases(jsondict, chatline)---append new message to json file
# previous_message(username) -------------- check if user submit button x2
# calc_score(corrected, username)---------- score each word then total
# calc_leaderboard(username, my_score) ---- reorder leaderboard
# parse_phrases(words)--------------------- check each word in message
# same(username)--------------------------- check if username already in use

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
    global chatters, userlog
    timer = time.time()
    print('start new thread', timer)
    new_loop = asyncio.new_event_loop()
    t = Thread(target=athread.start_loop, args=(new_loop,))
    t.start()
    new_loop.call_soon_threadsafe(athread.json_phrases, jsondict, chatline)
    print('after loop call, delay=', time.time() - timer)
    # check if each user still online
    new_loop.call_soon_threadsafe(athread.whois_online, userlog)
    found = athread.found
    if found:
        user0 = athread.decrement_userlog
        print('user0-79', user0)
        if user0 != '':
            del userlog[user0]  
            chatters += -1
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
        if my_score > score[k]:
            kpos = leaderboard.index(k)
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
    with open(sourcelist, "r") as word_list:  
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

def same(username):
    with open("data/users.txt", "r") as user_list:
        users = user_list.readlines()
        username += "\n"
        print ('same-',users, username)
        if username in users:
            return True
        else:
            return False
            
# ---------------4-VIEWS-----------------------------------------#
# '/'                       enter username then redirects to /username
# '/<username>'             main user chat page, handles form submits
# '/chat/messages'          updates each user with new messages
# '/chat/structure'         form to allow user to analyse any message line
# '/chat/test'              automated testing for structure analysis section

# user sign in page
@app.route('/', methods=["GET","POST"])
def index():
    global chatters, error_message, userlog
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
            if same(request.form["username"]):
                chatters -= 1
                error_message = "--> This username already taken - try another."
                flash("Sorry, but there was a problem:")
                return render_template("index.html", error=error_message)
            with open("data/users.txt", "a") as user_list:
                user_list.writelines(request.form["username"] + "\n")
            return redirect(request.form["username"]) 
        else:
            error_message = "--> Max Users exceeded - Access Denied"
            flash("Sorry, but there was a problem:")
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
        if request.form["form"] == "structure":         # 400 Bad Request: KeyError: 'cc'
                cc = request.form["cc"]     # perhaps hit submit by eror    
                sline = int(request.form["line"])
                sq = request.form["sq"]
                message = ""                # needed
                print("cc--", cc,sline,sq)
                structure.main(str(sline), sq, cc)
                print("run.py189 s-r=", structure.structure_result)
        else:
            if request.form["form"] == "message":
                message = request.form["message"]
                message = message.strip()
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
    global userlog, phrases
    if request.method == "GET":
        user = request.args["user"]
        timer = time.time()
        userlog[user] = timer    #timestamp user for later check if still online
    if len(phrases) > 5: # show only 10 messages
        phrase10 = []
        for i in range(5):
            phrase10.append(phrases[i-5])
        phrases = phrase10
    return render_template("messages.html", chat_messages=phrases,
                score=score, leaderboard=leaderboard)

# provide html to analyse phrase
@app.route('/chat/structure', methods=["GET","POST"])  
def struct(): 
    # "w3-include-html"
    result=structure.structure_result
    return render_template("structure.html", result=result)
    
@app.route('/chat/test', methods=["GET","POST"])  
def test():
    results = []
    if request.method == "POST":
        test = request.form['cc']
        if test == "test-s" or test == "test-se":
            sq = "stat"
        else:
            sq = "ques"
        for sline in range(1,4):        #using only lines 1-3, change this later
            structure.main(sline,sq,test)
            result=structure.structure_result
            results.append(result)
    else:
        result = "start test"
    return render_template("test.html", results=results)

if __name__ == '__main__': 
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
