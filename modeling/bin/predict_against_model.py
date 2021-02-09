#Using the model
import tensorflow as tf
from tensorflow import keras

#Reading Word Map
import json

#Text cleaning
from bin.text_cleaner import text_cleaner
#NTLK
from nltk.corpus import stopwords  # stopwords
from nltk.stem.porter import PorterStemmer #Stemming
from nltk.stem import WordNetLemmatizer # Lemmatization
import re, string #Text cleaning

#Word Vectorizer
from bin.word_vectorizer import word_vectorizer

# Variables

STOPWORDS = stopwords.words('english')
STOPWORDS = [word.translate(str.maketrans('','',string.punctuation)) for word in STOPWORDS] # 
LEMMING =  WordNetLemmatizer()
vocab_size = 100000

# To load the model into memory
def load_model(path):
    return tf.keras.models.load_model(path)

# Load the vocabulary into memory
def load_vocabulary(path):
    with open(path) as json_file:
        data = json.load(json_file)
    return data

def predict_results(cleaned_text,model,word_map,padding_len=700):
    vectorized_text = word_vectorizer(cleaned_text,word_map)
    padded_text = tf.keras.preprocessing.sequence.pad_sequences([vectorized_text],
                                                       padding='post',
                                                       maxlen=padding_len)
    tensor = tf.convert_to_tensor(padded_text)
    prediction = model.predict(tensor)
    return prediction
    
    