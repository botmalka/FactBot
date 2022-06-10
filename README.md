# FactBot
A fun hybrid (deep learning and rule-based) assistant and social companion

This project was developed as a way to create a functional chatbot that would be able to interact more like a human 

It uses spaCy and NLTK to decifer the confusing way people communicate using sentiment analysis and part-of-speech tagging

## Libraries: 
NLTK spaCy, speech_recognition, pyttsx3, (previously included gtts and may again)

requires Wolfram Engine (https://www.wolfram.com/engine/)

## Recent additions:
- added a short term memory for subjects of previous sentence to help with pronoun recognition
- gave the bot the ability to pull a sentence from an news article related to a topic, that contains the topic

## Future goals:
- finish functionality to recognize pronouns as previous subjects
- add a conversation history tracker (have variables set up, but need methods made)
- improve and vary responses made by chatbot
- add a database to store long-term information about certain subjects
- use named-entity recognition and addition APIs to learn about common topics from the internet 
