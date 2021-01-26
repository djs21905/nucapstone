#NTLK
from nltk.corpus import stopwords  # stopwords
from nltk.stem.porter import PorterStemmer #Stemming
from nltk.stem import WordNetLemmatizer # Lemmatization
import re, string #Text cleaning

from html_functions import ez_display as d

def text_cleaner(text_list,
                 STOPWORDS=[],
                 SIMPLE = True,
                 LEMMING=False,
                 STEMMING=False,
                 VERBOSE=0):
    
    if type(text_list) == str:
        new_text_list = [text_list]
    else:  
        new_text_list = [text.lower() for text in text_list] #lower case all
    
    if SIMPLE == True:
        #################REGEX####################
        url_regex = r'^https?:\/\/.*[\r\n]*' #To remove urls
        email_regex = r'\S*@\S*\s?' #Remove emails
        space_regex = r'\s+' #repeated characters
        regex_list = [url_regex,email_regex]

        for regex in regex_list:
            new_text_list = [re.sub(regex,' ',text,flags=re.MULTILINE) for text in new_text_list]

        d('Email and URLs removed')

        #################Non-ascii removal####################
        new_text_list = [text.encode('ascii',errors='ignore').decode() for text in new_text_list]

        d('Non-ascii characters removed')

        #################Special Characters ####################
        special_characters = 'ââ'
        punctuation = string.punctuation
        digits = string.digits
        removal_str = special_characters + punctuation + digits
        removal_len = len(removal_str)

        new_text_list = [text.translate(str.maketrans(removal_str,' '*removal_len)) for text in new_text_list]

        d('Special characters, punctuation, and digits removed')
        
        #################Extra Space Clean Up####################
        new_text_list = [re.sub(space_regex,' ',text,flags=re.MULTILINE) for text in new_text_list]

        d('Extra spaces removed')
    
    #################Word Analysis####################
    
    for index, new_text in enumerate(new_text_list): 
        words = new_text.split(' ')
        if len(STOPWORDS) > 0:
            words = [word for word in words if not word in STOPWORDS]
        
        if "lemmatizer" in str(type(LEMMING)).lower(): #Checking if lemmatizer is used
            words = [LEMMING.lemmatize(word) for word in words]
            if len(STOPWORDS) > 0:
                words = [word for word in words if not word in STOPWORDS]
            
        if "stem" in str(type(STEMMING)).lower(): #Checking if stemmer is used
#             words = [STEMMING.stem(word) for word in words]
            temp_words = []    
            for word in words:
                    try:
                        stem_word = STEMMING.stem(word)
                        temp_words.append(stem_word)
                    except:
    #                     d(f"{word} resulted in error")
                        temp_words.append(word)   
            words = temp_words
            if len(STOPWORDS) > 0:
                words = [word for word in words if not word in STOPWORDS]
        
        new_text = ' '.join(words)
        new_text_list[index] = new_text
    
    return new_text_list