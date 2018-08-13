# purpose: to analyse  Englishphrase as Subject + Verb + Object
import json
tobe = ['be', 'being', 'been', 'am', 'are', 'was', 'were']
tohave = ['have', 'having','had', 'has']
auxs = ['will', 'can', 'might', 'may', 'would', 'should', 'could']
verblist = "data/verbs.txt"

def getline(line):
     jphrase = {}
     jchat = {}
     with open("data/chatlines.json", "r") as jlines:
            jphrase = json.load(jlines)
     """ heroku error no iteritems      
     for k, v in jphrase.iteritems():
          print ("kv-", k, v)
     """     
     print("gline-", line)
     phrase = eval(jphrase[line])["message"]
     print("phrase17-",phrase)
     return phrase
     
def parse(phrase):
     words = phrase.split(' ')
     position = 0
     verb_position = []
     with open(verblist, "r") as verb_list:  
          verbs = verb_list.read().splitlines()   
          for word in words:
               print("word", word, "pos-", position)
               if word.lower() in verbs:
                    verb_position.append(position)
               position += 1
     print("vpos-", verb_position)       
            