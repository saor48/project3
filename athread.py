from threading import Thread
import asyncio
import athread
import time
import csv, json

# return values for main from structure
decrement_userlog = ""
found = False

print('--> athread.py', time.time()) 

def start_loop(loop):
    timer = time.time()
    print('start athread', timer)
    asyncio.set_event_loop(loop)
    #loop.run_until_complete()
    loop.run_forever()

def json_phrases(jsondict, chatline):
    timer = time.time()
    with open("data/chatlines.txt", "a") as chat:
            chat.writelines(str(chatline) + "\n")
    with open("data/chatlines.json", "w") as jfile:
            json.dump(jsondict, jfile)
    print('end filewrites delay=', time.time() - timer)
    
def whois_online(userlog):
    #check if no user get in last 15 secs => logged out
    global decrement_userlog, found
    found = False
    timer = time.time()
    print('whois-', userlog, timer)
    for user in userlog:
        print("log-", user,userlog[user])
        if userlog[user] + 15 < timer:
            print("at-", timer)
            remove(user)
            decrement_userlog = user
            found = True
    print('whois-', found)
    
def remove(user):
    print("popping-", user)
    user1 = user.split(' ')
    user = user1[1].lower() + "\n"
    with open("data/users.txt", "r") as user_list:
        users = user_list.readlines()
        users.pop(users.index(user))
    with open("data/users.txt", "w") as user_list:
        for user in users:
            user_list.writelines(user)  # \n already there
            
           