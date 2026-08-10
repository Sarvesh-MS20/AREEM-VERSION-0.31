# agent/executor.py
from tools.faiss_Search import faiss_search
from tools.calculator import calculator
from tools.web_search import web_search
from tools.chat import chat
from tools.whatsapp import whatsapp
from tools.weather import weather


def execute_tools(tool,tool_input,memory,user_id,context_memory ,used_faiss,scratchpad):
    if tool == "faiss_search":
        result = faiss_search(tool_input)

        if result == "NO CONTEXT":
            scratchpad+="FAISS FAILED , DO NOT USE FAISS AGAIN"
            webbing = web_search(tool_input)
            context_memory+=webbing+ "\n"
            return webbing , used_faiss, context_memory

        context_memory += result + "\n"
        used_faiss = True

        return result , used_faiss, context_memory

    elif tool == "calculator":
        return calculator(tool_input),used_faiss,context_memory

    elif tool == "whatsapp":
        return whatsapp(tool_input),used_faiss,context_memory

    elif tool == "weather":
        return weather(tool_input),used_faiss,context_memory

    elif tool == "chat":
        if used_faiss:
            return chat(tool_input,context_memory,memory,user_id),used_faiss,context_memory
        else:
            return chat(tool_input,"",memory,user_id),used_faiss,context_memory


    elif tool == "web_search":
        return web_search(tool_input),used_faiss,context_memory

    else:
        return "INVALID TOOL NGA EPDITHANO 😒🧐" ,used_faiss,context_memory
