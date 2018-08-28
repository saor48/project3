from threading import Thread
import asyncio
import athread
import time
import csv, json

print('--> athread.py', time.time()) 

def start_loop(loop):
    timer = time.time()
    print('start athread', timer)
    asyncio.set_event_loop(loop)
    #loop.run_until_complete()
    loop.run_forever()

#using new thread  for file writes and user still online updates from here==========
def json_phrases(jsondict, chatline):
    timer = time.time()
    with open("data/chatlines.txt", "a") as chat:
            chat.writelines(str(chatline) + "\n")
    with open("data/chatlines.json", "w") as jfile:
            json.dump(jsondict, jfile)
    print('end filewrites delay=', time.time() - timer)
            
   
#================================================