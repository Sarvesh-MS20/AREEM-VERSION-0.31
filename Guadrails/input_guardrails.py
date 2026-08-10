def is_query_safe(query:str)-> bool:

    un_safe_words = ["hack","murder","abuse","attack"]

    for word in un_safe_words:
        if word in query.lower():
            return False


    return True

