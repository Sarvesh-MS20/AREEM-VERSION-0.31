#agent/planner.py
import json
import re
from llm.client import safe_llm_calling
# -------------------------------------------------------------------------------------------
#                             PLANNER
# -------------------------------------------------------------------------------------------
def planner(query):
    prompt = f"""
    You are an HIGH LEVEL TASK PLANNER for an AI agent

    Your job is to break the user query into CLEAN,MINIMAL AND NON REDUNDANT steps

    ===========================================
          UNDERSTAND THE QUERY TYPE
    ===========================================
    classify the query into - 
        single task (OR) multiple task

    example:
    query :  calculate 2+2 
    -->single task

    query : calculate 2+67 and explain what is AI
    ---> multi task

    =============================================
                AVAILABLE TOOLS
    =============================================


    Break the user query into into muliple structured tasks

    - faiss_search ---> only for explanation , knowledge retrieval
    - calculator   ---> for mathematical calculation, mathematical operations 
    - chat  --->  Only for final answer , casual conversation , suggestions , ideas , greetings ,explanations
    - whatsApp ---> to open whatsApp if the query intends to
    - weather ---> to extract the weather info , climatic conditions
    - web_search ---> internet search (if information not available in faiss)

    ====================================
       PLANNING RULES(VERY IMPORTANT)
    ====================================
    1) Identify if the query has multiple tasks
    2) If the query can be solved in single step --> return ONLYY one task
    3) split the query only if needed
    4) DON't split simple queries
    5) Each task must:
       -  solve one clear goal
       - use only one tool per task

    6) tool selection rules:
       - web_search ---> unknown information/facts/information not in faiss
       - calculator ---> mathematical operations
       - faiss_search ----> knowledge retrieval
       - chat -----> casual conversation/explanations

    7) Never repeat same tasks
    8) keep only minimum tasks (MAX 3 tasks)

    9) IF multiple tasks exist:
        -->make sure all the tasks is needed to completely answer the query
        -->DO NOT stop after the first task

    =================================
      EXAMPLE 
    ===============================

    query : calculate 2+2 and what is AI ?

    Output:

    {{
    "tasks": [
     {{"goal" : "solve math" , "tool" : "calculator" , "input" : "calculate 2+2" }},
     {{"goal" : "explain AI" , "tool" : "faiss_search" , "input" : "what is AI?" }}
     {{"goal":"generate final answer","tool":"chat","input":"combine all the answers"}}
             ]
     }}

     query : hi how are you ?

    Output:

    {{
    "tasks": [
     {{"goal" : "greetings" , "tool" : "chat" , "input" : "hi how are you ?" }},
             ]
     }}
     
    ====================================    
        FINAL STEP RULE
    ====================================
    IF multiple tasks exist :

    Always add a final task

    example:
     ====================================    
        FINAL STEP RULE
    ====================================
    IF multiple tasks exist :

    Always add a final task

    example:
    {{"goal":"generate final answer","tool":"chat","input":"combine all the answers"}}


     =======================================
        STRICT ANSWER
     =======================================
     answer ONLY JSON

      {{
    "tasks": [
     {{"goal" : "....." , "tool" : "....." , "input" : "......" }},
             ]
     }}

    RULES FOR ANSWER:
    - No extra explanation
    - ONLY json

    =======================================
            QUERY
    =======================================
    {query}
    """
    messages = [{"role": "user", "content": prompt}]
    answer = safe_llm_calling(messages, temperature=0.2, max_tokens=150)

    match = re.search(r"\{.*?\}", answer, re.DOTALL)

    if match:
        try:
            json_ans = json.loads(match.group())
            return json_ans
        except:
            pass

    return {
        "tasks": [
            {
                "goal": "generate response", "tool": "chat", "input": query
            }
        ]
    }

