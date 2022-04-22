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
short_term = []
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
            break
        elif token.dep_ == "dobj": #finds direct object
            direct_object = token.orth_
            print('subject: ' + direct_object)
            break
        elif token.dep_ == "iobj": #finds indirect object
            indirect_object = token.orth_
            print('subject: ' + indirect_object)
            break
    if subject == '':
        print('no subject found...')
        
def find_obj(sentence):
    obj = ''
    for token in list(sentence)[::-1]:
        if token.dep_ == "iobj": #finds indirect object
            obj = token.orth_
            print('object: ' + obj)
            return        
        # elif token.dep_ == "nsubj": #finds subject
        #     subject = token.orth_
        #     print('object: ' + subject)
        #     return
        elif token.dep_ == "dobj": #finds direct object
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
       
    
#main
while utterance not in quit_words:
    try:
        utterance = listen()
        if utterance in quit_words:
            raise Exception("\nTalk to you later!")
        sentence = nlp(utterance)
        question = question_check(sentence)
        print('question: ' + str(question))
        print(sentiment(str(sentence)))
        if question is False:
            find_obj(sentence)
        #be_check(sentence)
        #speak(utterance) #repeats what you say - for testing
    except Exception as e:
        print(e)
