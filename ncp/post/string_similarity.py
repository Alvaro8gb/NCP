import difflib as dl

HOLD = 0.65

def replace_by_similar(words:list, values:list) -> list:
    replaced = []

    for word in words:
        word = word.lower()
        max_similarity = 0
        match_val = "None"

        for val in values:
            dl_value = dl.SequenceMatcher(None, val, word).ratio()
            if dl_value > max_similarity:
                match_val = val
                max_similarity = dl_value
        
        if max_similarity > HOLD:
            replaced.append(match_val)
        else: # If not found keep origninal
            replaced.append(word)
    
    return replaced