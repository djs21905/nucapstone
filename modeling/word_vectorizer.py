def word_vectorizer(row,col,map):
    clean_text = []
    for word in row: 
        try:
            word_int = map[col][word]
            clean_text.append(word_int)
        except:  
            continue
    return clean_text