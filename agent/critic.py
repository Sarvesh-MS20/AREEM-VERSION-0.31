#agent/critic.py
import json
import re
from llm.client import safe_llm_calling

# -------------------------------------------------------------------------------------------
#                             SELF REFLECTION (TOOL EVALUATION)
# -------------------------------------------------------------------------------------------

def critic_agent(query, answer):
    critic_prompt = f"""
    You are a STRICT AI CRITIC

    User query : {query}
    Agent answer : {answer}

    Check:
    1.Did it fully solve the query ?
    2.Any missing steps ?
    3.Any wrong info?

    DO NOT mark wrong for:
    - simple greetings
    - short confirmations
    - casual replies

    Respond only in JSON 

    {{"verdict" : "correct"}}
           or 
    {{"verdict" : "wrong", "reason" : "What is wrong ?"}}
"""

    messages = [{"role": "user", "content": critic_prompt}]
    answer = safe_llm_calling(messages, temperature=0.2, max_tokens=150)
    match = re.search(r"\{.*?\}", answer, re.DOTALL)

    if match:
        json_answer = match.group()
        try:
            ans = json.loads(json_answer)
            return ans
        except:
            return {"verdict": "wrong", "reason": "invalid JSON format"}

    return {"verdict": "wrong", "reason": "No JSON found"}
