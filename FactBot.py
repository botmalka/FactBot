# import os #these 5 import lines are only used with alternative speak function
# from os.path import exists
# import time
# import playsound
# from gtts import gTTS
import random, string, re
import pyttsx3
import speech_recognition as sr #from pip install SpeechRecognition
from duckduckgo_search import ddg, ddg_news
import wolframalpha
import spacy
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon') #downloads Valence Aware Dictionary and sEntiment Reasoner
#import textacy

utterance, response = "", None
quit_words = ['stop', 'bye', 'goodbye']
wolfram_app_id = 'K746RL-W3PKXK7GH6'
wolfram_client = wolframalpha.Client(wolfram_app_id)
sia = SentimentIntensityAnalyzer()
short_term, conversation = [], []
spacy_location = r"C:\ProgramData\Anaconda3\Lib\site-packages\en_core_web_md-3.2.0\en_core_web_md\en_core_web_md-3.2.0"
engine = pyttsx3.init()
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[1].id)
nlp = spacy.load(spacy_location)

""" Uncommenting this method and commenting the other "speak" will switch to Google's speech engine
it is currently having issues but was used in alpha and will be possibly used in later versions """
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
    print(text)
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

#determines if a sentence is a question or statement and returns boolean 
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
        print('99 no subject found...')
        return "", ""

#finds the object of the sentence 
def find_obj(sentence):
    obj = ''
    for token in list(sentence)[::-1]:
        if token.dep_ == "iobj": #finds indirect object
            obj = token.orth_
            print('object: ' + obj)
            return tuple([obj, token.pos_])       
        elif token.dep_ == "dobj": #finds direct object
            obj = token.orth_
            print('object: ' + obj)
            return tuple([obj, token.pos_]) 
        elif token.dep_ == "nsubj": #finds subject
            obj = token.orth_
            print('object: ' + obj)
            return tuple([obj, token.pos_])   
    if obj == '':
        print('118 no object found...')

    
#looks for forms of the word 'be' to link nouns with data
def be_check(sentence):
    for token in sentence:
        print(token.pos_)
        
        if token.pos_ == "AUX" and token.lemma_ in ["is", "be", "are"]:
            print("127 I found a be in this sentence at {}".format(token))
            #print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
      
def word_similarity(word1, word2):
    percent = len(set(word1) & set(word2)) / float(len(set(word1) | set(word2))) * 100
    return percent
            
#looks for named entities in the sentence
def named(sentence):
    my_ents = dict([(str(x), x.label_) for x in sentence.ents])
    print('I found a named entity!!')
    print(my_ents)
            
#searches duckduckgo news for info on keywords     
def news_search(keywords):
    response_type = ["I heard", "I read online", "I saw in the news"]
    response, responses = "", []
    key_filter = keywords.translate(str.maketrans('', '', string.punctuation)).split(" ")
    results = ddg_news(keywords, region='wt-wt', safesearch='Off', time='d', max_results=20)
    for articles in results:
        word_count = 0
        body = articles['body']
        nlp_body = nlp(body)
        sentence = list(nlp_body.sents)[0] 
        for word in str(sentence).split(" "):
            if word.lower() in key_filter:
                word_count += 1 
        if str(sentence)[-1] == ".":
            if sentence[0].pos_ == "PROPN": #keeps proper nouns capitalized
                response = random.choice(response_type) + " " + str(sentence[0:-1]) 
            else:
                response = random.choice(response_type) + " " + str(sentence[0]).lower() + " " + str(sentence[1:-1])
        if word_count >= 1:
            responses.append(response)
    return random.choice(responses)
    
#does sentiment analysis to determine what the user feels about a topic, which might help conversation   
def sentiment(sentence):
    feeling = sia.polarity_scores(sentence)
    return feeling      
       
#removes blanks or personal pronouns from short-term memory (list of subjects)
def clean_short_term(my_memory):
    remove_list = ["I", "you", "me"] #list of pronouns to dump
    for word in my_memory:
        if word in remove_list:
            my_memory.remove(word) #CURRENTLY NOT WORKING FOR NULL IN LIST
    my_memory = list(filter(None, my_memory)) #removes empties
    print("147 my_memory from clean_short_term: {}".format(my_memory))
    return my_memory

def return_query(info_type, info):
    
    return

def more_info(question):
    try:
        res = wolfram_client.query(question)
        answer = re.sub(r'\([^)]*\)', '', next(res.results).text)
        
    except Exception as e:
        print("I'm not sure.") 
        print(e)
    return answer
    


#asks to clarify if pronoun is used, ties pronoun to previous subject/object
def clarify_pronoun(pronoun, conversation):
    if pronoun in ["it", "It"]:
        question_type = "What"
    else:
        question_type = "Who"
    response = question_type + " do you mean by \'" + pronoun + "\'?"
    print("164 response: {}".format(response))
    return response
    
#calls needed methods to respond appropriately
def process_sentence(sentence, short_term):
    response = None
    short_term = clean_short_term(short_term)
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
        response = more_info(sentence)
    #be_check(sentence)
    #speak(utterance) #repeats what you say - for testing


    print("184 short term: {}".format(short_term))
    
    #currently working on adding POS checking between this and the find_sub method
    if len(short_term) >= 1:
        last_subject, last_subject_type = short_term[-1][0], short_term[-1][1]
        print(len(short_term))
        print(last_subject_type)
        if last_subject_type == "PRON":
            print("192 clarifying pronoun: {}".format(last_subject))
            response = clarify_pronoun(last_subject, conversation)
            #print("Who do you mean by \'{}\'?".format(short_term[0][0]))
    return response
    

#chatbot starts here
print("\n")
speak("Hi there, I'm ready to chat!")

#main - listens and responds using methods above
while utterance not in quit_words:
    try:
        utterance = listen()
        if utterance in quit_words:
            speak("talk to you later")
            raise Exception("\nTalk to you later!")
        sentence = nlp(utterance) 
        if sentence is not None:
            conversation.append(sentence)
            print("214 conversation: {}".format(conversation))
        else:
            print("216: sentence is none, I guess")
        response = process_sentence(sentence, short_term)
    except Exception as e:
        print(e)  
    if response is not None and utterance not in quit_words:
        speak(response)


    
    
