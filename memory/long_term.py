# memory/long_term.py
from db.db_ops import get_memory
from llm.client import calling_llm
import re
import json

def load_memory(user_id):
    memory = {}
    for key in ["name","goal","food","spouse"]:
        values = get_memory(user_id,key)
        if values:
            memory[key]=values[0]
    return memory



def smart_memory_storage_decider(query):
    prompt = f"""
    Decide if this is important long-term memory

    store ONLY if useful:
        - personal information
        - preferences
        - repeated behaviour

    User input:
    {query}

    Answer only:
     'YES' or 'NO'
    """
    messages = [{"role": "user", "content": prompt}]
    answer = safe_calling_llm(messages, temperature=0.2, max_tokens=50)

    if "YES" in answer:
        return True
    else:
        return False

def smart_memory_extractor(query, memory):
    prompt = f"""
You are an memory extraction AI.

Extract ONLY the important information.

Rules :
-Store only the long term useful info
-Ignore the temporary queries
-Keep it short and structured

Return JSON like:
{{
  "name" : "...",
  "goal" : "...",
  "food" : "...",
  "spouse" : "..."
}}
If nothing is important then return {{}}

User input:
{query}
"""

    messages = [{"role": "user", "content": prompt}]
    answer = safe_calling_llm(messages, temperature=0.2, max_tokens=50)
    match = re.search(r"\{.*?\}", answer, re.DOTALL)

    if match:
        try:
            data = json.loads(match.group())
            memory.update({k: v for k, v in data.items() if v})
        except:
            pass

    return memory


# remove the garbage memory
def clean_memory(memory):
    clean = {}

    for k, v in memory.items():
        if isinstance(v, str) and len(v) < 50:
            clean[k] = v

    return clean