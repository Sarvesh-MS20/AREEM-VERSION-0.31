def clean_output(text:str)-> str :
    banned_phrases = ["i dont know","maybe"]
    for phrase in banned_phrases:
        if phrase in text.lower():
            text = text.replace(phrase,"")

    return text