"""to fix
Heroku - not reseting users.txt -----
----->use sessions or----->reuse setInterval to check if user online
"""
"""to add
0.list of verbs, nouns
1. search phrase for verbs -done basic
2. second form input
3. user still online check = 5sec request recvd
"""
"""option
multi-thread searching 
asyncio - use for checking 3 above
"""
import os, asyncio
from flask import Flask, redirect, render_template, request, url_for, flash
import csv, json
import structure

app = Flask(__name__)
app.secret_key = os.urandom(24)
TEMPLATES_AUTO_RELOAD = False
PYTHONASYNCIODEBUG = 1

maxUSERS = 3
error_message = ""
phrases = []    
users = []  
jsondict = {}
chatters = 0    #current number of users online
line = 0       #enumerate each chat line
previous = {}   #store previous message for each user
score = {}      #hold current score for all users
leaderboard = [] #sorted list by top scorer
user_score = 0  #this username
print("userscore-", user_score)
sourcelist = "data/wordlist.txt"
     # adapted from https://github.com/first20hours/google-10000-english
sourcelist2 = "data/8K-english.txt"  

# ---------------6-Functions-----------------------------------------#
#  
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
    json_phrases(jsondict, chatline)

def json_phrases(jsondict, chatline):
    with open("data/chatlines.txt", "a") as chat:
            chat.writelines(str(chatline) + "\n")
    with open("data/chatlines.json", "w") as jfile:
            json.dump(jsondict, jfile)
    #start async userpage updates from here===============
   
    #================================================
    
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
#   '/'-'/<username>'-'/chat/messages'-'/chat/structure'

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
            with open("data/users.txt", "a") as user_list:
                user_list.writelines(request.form["username"] + "\n")
            return redirect(request.form["username"]) 
        else:
            error_message = "Max Users exceeded - No Access"
            flash("Max Users exceeded - Access Denied")
    return render_template("index.html", error=error_message)
 
@app.route('/<username>',  methods=["GET","POST"]) 
def username(username):
    global line, previous, score, user_score
    question = False
    name = username.title()
    with open("data/users.txt", "r") as user_list:  
        users = user_list.readlines()
    if request.method == "POST":
        if not request.form["message"]:
            cc = request.form["cc"]
            line = int(request.form["line"])
            sq = request.form["sq"]
            message = ""
            print("cc--", cc,line,sq)
            structure.main(str(line))
        else:
            message = request.form["message"]
        if str(message) != "":
            if str(message) != previous_message(username):     #dont reload POST data
                previous[str(username)] = str(message)
                line += 1
                words = message.split(' ')
                corrected = parse_phrases(words)
                add_phrase(username, corrected, line)
                #make def score instead
                user_score = calc_score(corrected, username)
    # ------ this is temp position---------
   # if line > 0:
      #  structure.main(str(line))
    #---------------------------   
    return render_template("chat.html", 
                username=name, chat_messages=phrases, users=users, 
                chatters=chatters, my_score=user_score, 
                score=score, leaderboard=leaderboard)

@app.route('/chat/messages', methods=["GET","POST"])  
def messages(): 
    #also here start a user timeout check -asyncio?
    return render_template("messages.html", chat_messages=phrases,
                score=score, leaderboard=leaderboard)

@app.route('/chat/structure', methods=["GET","POST"])  
def struct(): 
    # "w3-include-html"
    return render_template("structure.html")
  
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
