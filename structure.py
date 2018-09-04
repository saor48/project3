# purpose: to analyse an English phrase as Subject + Verb + Object
import json
structure_result = "result goes here"

tobe = ['be', 'being', 'been', 'am', 'are', 'is', 'was', 'were']
tohave = ['have', 'having','had', 'has']
modals = ['will', 'can', 'might', 'may', 'would', 'should', 'could']
auxs = ['am', 'are', 'is', 'was', 'were', 'have','had', 'has', 'do', 'does']
do = ['do', 'does']
wh1 = ['what', 'who', 'when', 'where', 'why', 'whose', 'how']
wh2 = ['which', 'how', 'whose']
wh3 = ['why']
pronoun = {'i':1, 'you':2, 'he':3, 'she':3, 'it':3, 'we':2, 'they':2}
SVagree = {1:('am', 'have'), 2:('are', 'have'), 3:('is', 'has')}
article = ['a', 'the']
"""
          
"""
verblist = "data/verbs.txt"
#position = []
verbs = ""

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
     print("split-", phrase, type(phrase))
     words = phrase.split(' ')
     return words
     
def parse(words):
     global verbs             #move fileread out of here
     #words = split(phrase)
     position = 0
     verb_position = []
     with open(verblist, "r") as verb_list:  
          verbs = verb_list.read().splitlines()   
          for word in words:
               print("word", word, "pos-", position)
               if word.lower() in verbs:
                    # if not preceded by article
                    if position != 0:
                         if words[position-1] not in article:
                              verb_position.append(position)
                    else:
                         verb_position.append(position)
               position += 1
     print("vpos-", verb_position)
     return verb_position
     
def svo(position, words):
     # ? improve by checking for verb in final position
          # problem = i want to sleep (time phrase)
     if position != []:
          vb = ""
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
          result = "svo ok"
          return((sj, vb, ob), (spos, obpos), result)
     else:
          result = "no verb"
          x="x"
          return((x,x,x), (0, 0), result)

def vso(vpos, words):
     #words = split(phrase)
     print("svo-w?p-", words, len(words), type(words))
     if words[1] in wh1:
          if words[2] in auxs:
               return 'maybe 1verb -wh1'    
          else:
               return 'should have verb(be,have) in position 2'
     elif words[1] in wh2:
          if words[3] in auxs:
               return 'maybe 1verb -wh2'
     elif vpos[0] == 1:
          return 'maybe 1verb'
     else:
          return 'should start with auxiliary'
          
def asvo(vpos, words):
     print("asvo-w?p-", words)
     # wh- questions
     if words[1] in wh1:
          if words[1] in wh2:
               if words[3] in auxs:
                    return 'maybe wh2'            #wh2
          else:
               if words[2] in auxs:               #wh1
                    if words[3] not in verbs:
                         if vpos[-1] > 2:
                              return 'maybe wh1'
                    else:
                         return 'subject should follow auxiliary -wh'
     # standard questions = aux and main verb
     if words[1] in auxs:                              #aux
          if words[2] not in verbs:          
               return 'maybe aux+verb'
          else:
               return 'subject should follow auxiliary'
     else:
          return 'no auxiliary verb in position 2'

def agreement(sj, vb):
     print('agreement-sjvb', sj, vb)
     sb = sj.strip()
     vb1 = vb.strip()
     print('agreement-sb', sb, vb1)
     if sb in pronoun:
          key = pronoun[sb]
          if vb1 in SVagree[key]:
               return 'SVagree'
          else:
               return 'SVagree incorrect'

def format_result(result):
     global structure_result
     # in agreement
     if result == 'SVagree':
          structure_result = 'Subject and Verb in agreement'
     if result == 'SVagree incorrect':
          structure_result = 'Subject and Verb are not in agreement'
     # in asvo
     if result == 'no auxiliary verb in position 2':
          structure_result = 'Position 2 should be an auxiliary verb'
     if result == 'subject should follow auxiliary':
          structure_result = 'The subject should follow the auxiliary verb'
     if result == 'maybe aux+verb':
          structure_result = 'Perhaps correct - no error found for format'
     # in asvo - wh-questions
     if result == 'subject should follow auxiliary -wh':
          structure_result = 'The subject should follow the auxiliary verb'
     if result == 'maybe wh1':
          structure_result = 'Perhaps correct - no error found for format'
     if result == 'maybe wh2':
          structure_result = 'Perhaps correct - no error found for format'
     # in svo
     if result == 'svo ok':
          structure_result = 'Perhaps correct - no error found for format'
     if result == 'no verb':
          structure_result = 'This statement has no verb'    
     # in vso 
     if result == 'should start with auxiliary':
          structure_result = 'A question should start with an auxiliary verb'
     if result == 'maybe 1verb':
          structure_result = 'Perhaps correct - no error found for format'
     if result == 'maybe 1verb':
          structure_result = 'Perhaps correct - no error found for format'
     if result == 'maybe 1verb -wh2':
          structure_result = 'Perhaps correct - no error found for format'
     if result == 'should have verb(be,have) in position 2':
          structure_result = 'Position 2 should be a verb(be/have)'
     if result == 'maybe 1verb -wh1':
          structure_result = 'Perhaps correct - no error found for format'
     # in main
     if result == 'no verb -ques':
          structure_result = 'This question has no verb'
     if result == 'is too short for asvo':
          structure_result = 'This question is missing at least one word'
     if result == 'too short to challenge':
          structure_result = 'Challenges must have at least three words'
     if result == '[] word':
          structure_result = 'Challenges cannot have [] words'
          
def main(line, sq, cc):
     global structure_result
     phrase = getline(line).lower()
     print("main-phrase-", phrase)
     words = split(phrase)
     vpos = parse(words)
     if len(words) > 3:  # space plus 2
          if sq =="stat":
               output = svo(vpos, words)
               output1 = output[0]
               sj = output1[0]
               vb = output1[1]
               print(agreement(sj, vb))
               result = output[2]
          if sq =="ques":
               if len(vpos) == 0:
                    result = "no verb -ques"
               if len(vpos) == 1:
                    result = vso(vpos, words)
               if len(vpos) > 1:
                    if len(words) > 3:                
                         result = asvo(vpos, words)
                    else:
                         result = 'is too short for asvo'
     else:
         result = "too short to challenge"
     for word in words:
          if len(word) > 0:
               if word[0] == '[':
                    result = "[] word"
     print('st.py main, line-', line, result, 'Checked as a ', sq)
     format_result(result)
     structure_result = line + "> " + structure_result
     print("s-r=", structure_result)
     