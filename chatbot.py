import nltk
from nltk.stem import WordNetLemmatizer

# this will cut down the word to the stem, e.g like, liking, likeable will all be compared as "like"
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from tensorflow.keras.models import load_model

model = load_model('MentalHealth_model.h5')
import json
import random

intents = json.loads(open("intents.json", encoding='utf-8').read())
words = pickle.load(open('words.pkl', 'rb'))
tags = pickle.load(open('classes.pkl', 'rb'))

bot_name = "OreoBot"
ERROR_THRESHOLD = 0.25


def clean_sentence(sentence):
    sentence_with_words = nltk.word_tokenize(sentence)
    sentence_with_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_with_words]
    return sentence_with_words


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bag_of_words(sentence):
    sentence_with_words = clean_sentence(sentence)
    bag_of_words = [0] * len(words)
    for s in sentence_with_words:
        for i, word in enumerate(words):
            if word == s:
                 bag_of_words[i] = 1
                 print(i)
    return np.array( bag_of_words)


def prediction(sentence):
    # filter out predictions below a threshold
    bow = bag_of_words(sentence)
    outcome = model.predict(np.array([bow]))[0]
    print(outcome)
  
    filter_results = [[i, r] for i, r in enumerate(outcome) if r > ERROR_THRESHOLD]

    filter_results.sort(key=lambda x: x[1], reverse=True)

    return_list = []
    for r in filter_results:
        return_list.append({"intent": tags[r[0]], 'probability': str(r[1])})  
    return return_list


def response(intents_list, intents_json): 
        
    try:
        tag = intents_list[0]['intent']
        probability = intents_list[0]['probability']

        list_of_intents = intents_json['intents']
        

        if probability > str(0.25): 
            for i in list_of_intents:
                if (i['tag'] == tag):
                    response_result = random.choice(i['responses'])
                    break   
             
    except Exception:
        response_result = "Sorry i dont understand, please ask me something else"

    finally: 
        return response_result
        
    

def chat(msg):
    pred = prediction(msg)
    #print(ints[0]['probability']) # this was for testing purposes
    result = response(pred, intents)
    return result
