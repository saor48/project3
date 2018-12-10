# purpose: to analyse an English phrase as Subject + Verb + Object =svo
# questions have form = asvo, where a = auxiliary verb.
# questions can also be vso and wh-word + asvo/vso
# not yet added - imperatives

import json
structure_result = "result goes here"

tobe = ['be', 'being', 'been', 'am', 'are', 'is', 'was', 'were']
tohave = ['have', 'having','had', 'has']
modals = ['will', 'can', 'might', 'may', 'would', 'should', 'could']
auxs = ['am', 'are', 'is', 'have', 'has', 'do', 'does','was', 'were','had','did']
auxs1 = ['am', 'are', 'is', 'have', 'has', 'do', 'does']
aux2 =['was', 'were','had', 'did']
aux3 = ['are', 'is', 'have', 'has']
do = ['do', 'does', 'did']
wh1 = ['what', 'who', 'when', 'where', 'why', 'whose', 'how']
wh2 = ['which', 'how', 'whose']
why = ['why']
how = ['how']
pronoun = {'i':1, 'you':2, 'he':3, 'she':3, 'it':3, 'we':2, 'they':2}
SVagree = {1:('am', 'have', 'do'), 2:('are', 'have', 'do'), 3:('is', 'has', 'does')}
article = ['a', 'the']
     #quantifiers should include all numbers!!!!!!
quantifier = ['no', 'some', 'any', 'much', 'many', 'little', 'few']
prep = ['to', 'with']

verblist = "data/verbs.txt"
verbs = ""

#============---------10 functions------=========================
# def getline(line)............read line from json file
# def split(phrase)............split phrase into words
# def punctuation(words).......remove ? from last word
# def parse(words).............find position of verbs in phrase
# def svo(position, words).....find subject before and object after verb
# def vso(vpos, words).........check structure for (wh-word)vso
# def asvo(vpos, words)........check structure for (wh-word)asvo
# def agreement(sj, vb)........sv agreement only for pronoun+be/have
# def format_result(result)....text value for display
# def main(line, sq, cc) ......analyse user inputs then call fns as needed
# ============--------------------------------==================
def gettestline(line, test):
     phrase = " "
     line = line-1
     if test == "test-s":
          with open("data/tests/statements.txt", "r") as lines:
            phrases = lines.readlines()
            phrase += phrases[line].rstrip()
     if test == "test-se":
          with open("data/tests/serror.txt", "r") as lines:
            phrases = lines.readlines()
            phrase += phrases[line].rstrip()
     if test == "test-q":
          with open("data/tests/questions.txt", "r") as lines:
            phrases = lines.readlines()
            phrase += phrases[line].rstrip()
     if test == "test-qe":
          with open("data/tests/qerror.txt", "r") as lines:
            phrases = lines.readlines()
            phrase += phrases[line].rstrip()
     return phrase

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
     print("gline2", jphrase)
     if line in jphrase:
          phrase = eval(jphrase[line])["message"]
     else:
          phrase = "Invalid line number:" + str(line)
     print("phrase54-",phrase)
     return phrase

def split(phrase):
     print("split-", phrase, type(phrase))
     words = phrase.split(' ')
     return words

def punctuation(words):
     for word in words:
          #remove ? from last word
          if word == words[-1]:
               if word[-1] == '?':
                    word = word[:-1] 
                    words[-1] = word
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
                    # if not preceded by article or quantifier 
                    if position > 1:
                         x = words[position-1]
                         #this line not very good!!!
                         if x not in article and x not in quantifier:
                              if len(verb_position) > 0:
                                   # allow object to be verb participle
                                   # not eg -is closed- but -have you closed-
                                   # also eg -can i help
                                   v1 = words[verb_position[0]]
                                   pv1 = verb_position[0]
                                   print('v1pv1-',v1,pv1)
                                   if v1 in aux3 or v1 in modals:
                                        if pv1 != position-1:
                                             print('inif-pos', position)
                                             verb_position.append(position)
                              else:
                                   verb_position.append(position)
                    else:
                         verb_position.append(position)
               position += 1
     print("vpos-", verb_position)
     return verb_position
     
def svo(position, words):
     # ? improve by checking for verb in final position
          # problem = i want to sleep (time phrase)
     # remove non adjacent verb to have object --but?need to improve this
     # remove in; the shop is now -closed-
     if len(position) == 2:
          if position[1] - position[0] > 1 :
               print('svo-vpos-', position)
               position.pop(1)
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
          if position[0] == 1:
               result = 'no subject'
          elif obpos == len(words):
               result = 'no object'
          else:
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
          elif words[1] not in wh2:
               return 'should have verb(be,have) in position 2'
     if words[1] in wh2:           # expand and new function!!!!!!+asvo!!
          if words[3] in auxs:               #how much does..
               return 'maybe 1verb -wh2'
          else:                              #how many books do..
               return 'maybe 1verb -wh2'       # further analysis reqd!!!!
     elif vpos[0] == 1:
          print('vso-',words[-1],words[-2])
          print(words[-1] in pronoun and words[-2] not in prep)
          if words[-1] in pronoun and words[-2] not in prep:
               return 'subject in wrong position'
          else:
               return 'maybe 1verb'
     else:
          return 'should start with auxiliary'
          
def asvo(vpos, words):
     print("asvo-w?p-", words)
     # wh- questions
     if words[1] in wh1:
          if words[1] in wh2:
               if words[3] in auxs:               #wh2['which', 'how', 'whose']
                    return 'maybe wh2' 
               else:
                    return 'maybe wh2'            # further analysis
          elif words[2] in auxs:                  #wh1
               if words[3] not in verbs:
                    if vpos[-1] > 2:
                         return 'maybe wh1'
               else:
                    return 'subject should follow auxiliary -wh'
          else:
               return 'no auxiliary verb in position 2 - wh'               
     # standard questions = aux and main verb
     if words[1] in auxs or words[1] in modals:             #aux/modals
          if words[2] not in verbs:          
               return 'maybe asv'
          else:
               return 'subject should follow auxiliary'
               
     

def agreement(sj, vb):
     print('agreement-sjvb', sj, vb)
     sb = sj.strip()
     vb1 = vb.strip()
     if sb in pronoun:
          key = pronoun[sb]
          if vb1 in SVagree[key]:
               return 'SVagree'
          else:
               if vb1 in auxs1:
                    return 'SVagree incorrect'
     else:
          return " "

def format_result(result):
     global structure_result
     # in asvo
     if result == 'no auxiliary verb in position 2 - wh':
          structure_result = 'Position 2 should be an auxiliary verb'
     if result == 'subject should follow auxiliary':
          structure_result = 'The subject should follow the auxiliary verb'
     if result == 'maybe asv':
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
     if result == 'no subject':
          structure_result = 'This statement has no subject'
     if result == 'no object':
          structure_result = 'This statement has no object'     
     if result == 'no verb':
          structure_result = 'This statement has no verb'    
     # in vso 
     if result == 'should start with auxiliary':
          structure_result = 'A question should start with an auxiliary verb'
     if result == 'maybe 1verb':
          structure_result = 'Perhaps correct - no error found for format'
     if result == 'maybe 1verb -wh2':
          structure_result = 'Perhaps correct - no error found for format'
     if result == 'should have verb(be,have) in position 2':
          structure_result = 'Position 2 should be a verb(be/have/do)'
     if result == 'maybe 1verb -wh1':
          structure_result = 'Perhaps correct - no error found for format'
     if result == 'subject in wrong position':
          structure_result = 'The subject is in the wrong position'    
     # in main
     if result == 'no verb -ques':
          structure_result = 'This question has no verb'
     if result == 'is too short for asvo':
          structure_result = 'This question is missing at least one word'
     if result == 'too short to challenge':
          structure_result = 'Challenges must have at least three words'
     if result == '[] word':
          structure_result = 'Challenges cannot have [] words'
     # in agreement--main
     if result == 'SVagree incorrect':
          structure_result = "Subject and Verb are not in agreement"
          
def main(line, sq, cc):
     global structure_result, agree
     if cc == "chal":
          phrase = getline(line).lower()
     if "test" in cc:
          phrase = gettestline(line, cc).lower()
     print("main-phrase-", phrase)
     words = split(phrase)
     words = punctuation(words)
     vpos = parse(words)
     if len(words) > 3:  # space plus 2
          if sq =="stat":
               output = svo(vpos, words)  #return((sj, vb, ob), (spos, obpos), result)
               output1 = output[0]
               sj = output1[0]
               vb = output1[1]
               print(agreement(sj, vb))
               result = output[2]
               if result == "svo ok":
                    agree = agreement(sj, vb)
                    if agree == 'SVagree incorrect':
                         result = agree
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
     structure_result = str(line) + "> " + structure_result
     print("s-r=", structure_result)
     