
def prompt_builder(query, history_text, context, memory, memory_text):

    prompt = f"""
    YOU ARE AN INTELLIGENT AI SYSTEM 

    CONVERSATION SO FAR : {history_text}

    GO THROUGH THE CONTEXT IF NEEDED : {context}

    LOOK AT THE USER QUERY : {query}

    MEMORY : 

    - Name : {memory.get("name", "unknown")}
    - City : {memory.get("city", "unknown")}
    - Preferences : {memory.get("preferences", "unknown")}
    - Goal : {memory.get("goal", "unknown")}

    Relevant past memories:
    {memory_text}

    RULES :
    1) Go through the chat history before answer the queries. 
    2) Adapt to the chat history to connect to previous conversation.
    3) Go through the context if needed .


    ANSWER THE QUERIES CAREFULLY 
"""
    return prompt
