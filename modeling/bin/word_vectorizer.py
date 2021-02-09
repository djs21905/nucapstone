def word_vectorizer(cleaned_text,map):
    clean_text = []
    for word in cleaned_text:
        try: 
            word_int = map[word]
            clean_text.append(word_int)
        except:
            continue
    return clean_text

def word_vectorizer_columns(row,col,map):
    clean_text = []
    for word in row: 
        try:
            word_int = map[col][word]
            clean_text.append(word_int)
        except:  
            continue
    return clean_text