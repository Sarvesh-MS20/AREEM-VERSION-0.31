#llm/client.py
from  openai import OpenAI
import json

# ------------------------------------------------------
#                   API SETUP
# ------------------------------------------------------

with open('api_key.json','r')as f:
    config = json.load(f)

api_key = config['key']

# ------------------------------------------------------
#                   MODEL INITIALIZATION
# ------------------------------------------------------
client = OpenAI(
    api_key = api_key,
    base_url = "https://api.groq.com/openai/v1"
)

# ------------------------------------------------------
#                   CALLING LLM
# ------------------------------------------------------
def calling_llm(messages, temperature=0.2, max_tokens=50):
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"LLM ERROR (attempt {attempt + 1}):", e)
            time.sleep(1)
    return "ERROR"




def safe_llm_calling(messages, temperature=0.2, max_tokens=50):
    retries = 3
    for attempt in range(retries):
        try :
            response = calling_llm(messages, temperature, max_tokens)

            # to chech whether a response is valid or not
            if response and len(response.strip())>0 :
                return response

        except Exception as e:
            print(f"some kinda ERROR {e}")


        time.sleep(1)

    return "ERROR"



