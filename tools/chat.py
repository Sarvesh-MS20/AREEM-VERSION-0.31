#tools/chat.py
from db.db_ops import get_chat_history
from memory.vector_memory import extract_memory
from prompt_builder import prompt_builder
from llm.client import calling_llm

def chat(query, context_memory ,memory,user_id):
    history = get_chat_history(user_id)
    history_text = "\n".join(f" role :{role} , message :{message}"for role,message in history[-4:])
    relevant_memory = extract_memory(query)
    relevant_memory_clear = "\n".join(relevant_memory)
    prompt = prompt_builder(query,history_text,context_memory,memory,relevant_memory_clear)
    message = [{"role":"user","content":prompt}]
    result = calling_llm(message)
    return result

