import nltk
nltk.download('punkt')
nltk.download('wordnet')

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

import json
import pickle
import random

words = []
tags = []
documents = []
ignore_symbols = ['?', '!', '.', ',']
json_file = open('intents.json', encoding='utf-8').read()
intents = json.loads(json_file)


# here we are iterating over the intents
for intent in intents['intents']:
    for pattern in intent['patterns']:
        list_of_words = nltk.word_tokenize(pattern)
        words.extend(list_of_words)
        documents.append((list_of_words, intent['tag']))
        if intent['tag'] not in tags:
            tags.append(intent['tag'])


words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_symbols]


# eliminating duplicates
words = sorted(set(words))
tags = sorted(list(set(tags)))

# saving each of the words and tags into files.
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(tags, open('classes.pkl', 'wb'))

# initializing training data
training_list = []
# this will be an list of zeros
template = [0] * len(tags)


# here is where we are going to start converting the data to numerical data, so that the neural network understands it.
for doc in documents:
    bag_of_words = []
    patterns = doc[0]
    patterns = [lemmatizer.lemmatize(word.lower()) for word in patterns]

    for word in words:
        bag_of_words.append(1) if word in patterns else bag_of_words.append(0)

    output_row = list(template)
    output_row[tags.index(doc[1])] = 1
    training_list.append([bag_of_words, output_row])


random.shuffle(training_list)
training_list = np.array(training_list)

# create train and test lists. X - patterns, Y - intents
training_x = list(training_list[:, 0])
training_y = list(training_list[:, 1])
print("Training data has been created")


model = Sequential()
model.add(Dense(425, input_shape=(len(training_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(250, activation='relu')) 
model.add(Dropout(0.5))
model.add(Dense(len(training_y[0]), activation='softmax'))
model.summary()


# here we are compiling model. stochastic gradient decent with Nesterov accelerated gradient gives good results for the model
stochastic_gradient_descent= SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)  
model.compile(loss="categorical_crossentropy", optimizer=stochastic_gradient_descent, metrics=['accuracy'])

# fitting and saving model
hist = model.fit(np.array(training_x), np.array(training_y), epochs=200, batch_size=5, verbose=1)
model.save('MentalHealth_model.h5', hist)
print("Done")

