import os
from os.path import exists
import time
import playsound
import pyttsx3
import speech_recognition as sr #from pip install SpeechRecognition
from gtts import gTTS
import spacy
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon') #downloads Valence Aware Dictionary and sEntiment Reasoner
#import textacy

utterance = ""
quit_words = ['stop', 'bye']
sia = SentimentIntensityAnalyzer()
short_term, conversation = [], []
spacy_location = r"C:\ProgramData\Anaconda3\Lib\site-packages\en_core_web_md-3.2.0\en_core_web_md\en_core_web_md-3.2.0"
engine = pyttsx3.init()
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[1].id)
nlp = spacy.load(spacy_location)

print("\nHi there, I'm ready to chat!")


# def speak(text):
#     tts = gTTS(text=text)
#     filename = r'c:\users\tori\documents\voiceclips\{}.mp3'.format(text.replace(' ', '_')) 
#     if exists(filename):    
#         playsound.playsound(filename)
#         print("found " + filename)
#     else:
#         print("didn't find " + filename)
#         tts.save(filename)
#         time.sleep(0.1)
#         playsound.playsound(filename)


#output via text-to-speech
def speak(text):
    engine.say(text)
    engine.runAndWait()
    #sentence = nlp(text)
    
#this method listens on the system-set microphone and returns words if detected
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        
        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            if e in ['',' ']:
                print("Exception: " + str(e))
            else:
                print("I can't hear you.")       
    return said


def question_check(sentence):
    words = list(enumerate(sentence.text.split(' ')))
    question = False
    if len(words) <= 1:
        return question
    for i, token in words:
        print(str(i) + ': ' + token + ' ' + sentence[i].tag_ + ' ' + sentence[i].pos_)
    if (sentence[0].tag_[0] == "W") or (sentence[0].pos_ == "INTJ" and sentence[1].tag_[0] == "W"):
        question = True
    if (sentence[0].pos_ == "AUX" and sentence[1].pos_ == "PRON"):
        question = True
    if (sentence[0].pos_ == "INTJ" and sentence[1].pos_ == "AUX" and sentence[2] == "PRON"):
        question = True
    print(' ')
    return question        
    


#finds the subject of the sentence and finds more information on it 
def find_sub(sentence):
    subject = ''
    for token in sentence:
        if token.dep_ == "nsubj": #finds subject
            subject = token.orth_
            print('subject: ' + subject)
            return tuple([subject, token.pos_])
        elif token.dep_ == "dobj": #finds direct object
            direct_object = token.orth_
            print('subject: ' + direct_object)
            return tuple([direct_object, token.pos_])
        elif token.dep_ == "iobj": #finds indirect object
            indirect_object = token.orth_
            print('subject: ' + indirect_object)
            return tuple([indirect_object, token.pos_])
    if subject == '':
        print('no subject found...')
        return "", ""
        
def find_obj(sentence):
    obj = ''
    for token in list(sentence)[::-1]:
        if token.dep_ == "iobj": #finds indirect object
            obj = token.orth_
            print('object: ' + obj)
            return        
        elif token.dep_ == "dobj": #finds direct object
            obj = token.orth_
            print('object: ' + obj)
            return
        elif token.dep_ == "nsubj": #finds subject
            obj = token.orth_
            print('object: ' + obj)
            return        
    if obj == '':
        print('no object found...')

    
#looks for forms of the word 'be' to link nouns with data
def be_check(sentence):
    for token in sentence:
        print(token.pos_)
        
        if token.pos_ == "AUX" and token.lemma_ in ["is", "be", "are"]:
            print("I found a be in this sentence at {}".format(token))
            #print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
            
            
#looks for named entities in the sentence
def named(sentence):
    print('I found a named entity!!')
            
    
    
#does sentiment analysis to determine what the user feels about a topic, which might help conversation   
def sentiment(sentence):
    feeling = sia.polarity_scores(sentence)
    return feeling      
       
def clean_short_term(my_memory):
    remove_list = ["", "I", "you", "me"]
    for word in my_memory:
        if word in remove_list:
            my_memory.remove(word) #CURRENTLY NOT WORKING FOR NULL IN LIST
    print("my_memory from clean_short_term: {}".format(my_memory))
    return my_memory

def return_query(info_type, info):
    
    return

def more_info():
    
    return

def clarify_pronoun(pronoun, conversation):
    if pronoun in ["it", "It"]:
        question_type = "What"
    else:
        question_type = "Who"
    print("{} do you mean by \'{}\'?".format(question_type, pronoun))
    print(conversation)
    return
    
#main
while utterance not in quit_words:
    try:
        utterance = listen()
        if utterance in quit_words:
            raise Exception("\nTalk to you later!")
        sentence = nlp(utterance) 
        question = question_check(sentence) #type is boolean
        print('question: ' + str(question))
        print(sentiment(str(sentence)))
        if question is False:
            subject, subject_type = find_sub(sentence) 
            short_term.append(tuple([subject, subject_type])) #CURRENT LINE BEING MODIFIED
            print("subject: {} & type: {}".format(short_term[0][0], short_term[0][1]))            
            print(short_term)
            find_obj(sentence)
        else:
            find_sub(sentence)[0]
        #be_check(sentence)
        #speak(utterance) #repeats what you say - for testing
    except Exception as e:
        print(e)
    short_term = clean_short_term(short_term)
    print("short term: {}".format(short_term))
    
    #currently working on adding POS checking between this and the find_sub method
    if len(short_term) >= 1:
        print(len(short_term))
        print(short_term[-1][1])
        if short_term[-1][1] == "PRON":
            print("clarifying pronoun: {}".format(short_term[-1][0]))
            clarify_pronoun(short_term[-1][0], conversation)
            #print("Who do you mean by \'{}\'?".format(short_term[0][0]))
    
