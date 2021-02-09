#NTLK
from nltk.corpus import stopwords  # stopwords
from nltk.stem.porter import PorterStemmer #Stemming
from nltk.stem import WordNetLemmatizer # Lemmatization
import re, string #Text cleaning

from .html_functions import ez_display as d

STOPWORDS = stopwords.words('english')
STOPWORDS = [word.translate(str.maketrans('','',string.punctuation)) for word in STOPWORDS] # 

def text_cleaner(text_list,
                 STOPWORDS=STOPWORDS,
                 SIMPLE = True,
                 YEARS = True,
                 MIN_CHAR_LENGTH = 3,
                 LEMMING=False,
                 STEMMING=False,
                 VERBOSE=False):
    
    if type(text_list) == str:
        new_text_list = [text_list.strip()]
    else:
        new_text_list = text_list
    
    if SIMPLE == True:
        #################REGEX####################
        url_regex = r'^https?:\/\/.*[\r\n]*' #To remove urls
        email_regex = r'\S*@\S*\s?' #Remove emails
        space_regex = r'\s+' #repeated characters
        regex_list = [url_regex,email_regex]

        for regex in regex_list:
            new_text_list = [re.sub(regex,' ',text,flags=re.MULTILINE) for text in new_text_list]
            
        if VERBOSE:
            d('Email and URLs removed')

        #################Non-ascii removal####################
        new_text_list = [text.encode('ascii',errors='ignore').decode() for text in new_text_list]
        
        if VERBOSE:
             d('Non-ascii characters removed')

        #################Special Characters ####################
        special_characters = 'ââ'
        punctuation = string.punctuation
        removal_str = special_characters + punctuation
        removal_len = len(removal_str)

        new_text_list = [text.translate(str.maketrans(removal_str,' '*removal_len)) for text in new_text_list]

        if VERBOSE:
             d('Special characters and punctuations removed')
        
        #################Extra Space Clean Up####################
        new_text_list = [re.sub(space_regex,' ',text,flags=re.MULTILINE) for text in new_text_list]

        if VERBOSE:
            d('Extra spaces removed')
            
    if YEARS == True:
        for index, new_text in enumerate(new_text_list):
            words = new_text.split(' ')
            temp_words = []
            for word in words:
                if word.isalpha():
                    temp_words.append(word)
                if (word.isdigit()) and (len(word)==4):
                    temp_words.append(word)
            new_text = ' '.join(temp_words)
            new_text_list[index] = new_text
        
        if VERBOSE:
            d('Non-year digits removed')
    
    if MIN_CHAR_LENGTH != False:
        for index, new_text in enumerate(new_text_list):
            words = new_text.split(' ')
            words = [word for word in words if len(word) > MIN_CHAR_LENGTH]
            new_text = ' '.join(words)
            new_text_list[index] = new_text
        
        if VERBOSE:
            d(f'All words less than or equal to {MIN_CHAR_LENGTH} removed')
        
    #################Word Analysis####################
    
    for index, new_text in enumerate(new_text_list): 
        words = new_text.split(' ')
        if type(STOPWORDS) == list:
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