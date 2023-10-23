import difflib as dl

HOLD = 0.65

def replace_by_similar(word:str, values:list) -> list:
    replaced = word

    word = word.lower()
    max_similarity = 0
    match_val = "None"

    for val in values:
        dl_value = dl.SequenceMatcher(None, val, word).ratio()
        if dl_value > max_similarity:
            match_val = val
            max_similarity = dl_value
    
    if max_similarity > HOLD:
        replaced = match_val 
    
    return replaced