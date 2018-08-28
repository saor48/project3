# purpose: to analyse an English phrase as Subject + Verb + Object
import json
tobe = ['be', 'being', 'been', 'am', 'are', 'is', 'was', 'were']
tohave = ['have', 'having','had', 'has']
modals = ['will', 'can', 'might', 'may', 'would', 'should', 'could']
auxs = ['am', 'are', 'is', 'was', 'were', 'have','had', 'has']
"""
          
"""
verblist = "data/verbs.txt"
#position = []

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
     print("phrase24-",phrase)
     return phrase

def split(phrase):
     words = phrase.split(' ')
     return words
     
def parse(phrase):
     words = split(phrase)
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
     return verb_position
     
def svo(position, phrase):
     if position:
          vb = ""
          words = split(phrase)
          for pos in position:
               print("svopos-",pos)
               print(words)
               vb += words[int(pos)] + " "
          print(" verb=", vb)
          sj = ""
          spos = int(position[0])
          for i in range(spos) :
               sj += words[i] + " "
          print(" subj=", sj)
          ob = ""
          obpos = int(position[-1]) + 1
          for i in range(obpos, len(words), 1) :
               ob += words[i] + " "
               print(" obj=", ob)
     else:
          return()
     return(sj, vb, ob)

def main(line):
     phrase = getline(line)
     vpos = parse(phrase)
     svo(vpos, phrase)
            