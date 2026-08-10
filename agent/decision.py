#agent/decision.py
import json
import re
from llm.client import safe_llm_calling

def decide_agent(user_query, scratchpad):
    decision_prompt = f"""
    You are an intelligent AI agent that solves problems step by step using tools.

==================================
SCRATCHPAD (PAST STEPS)
==================================

The scratchpad contains previous steps in this format:

Step X:
thought: ...
tool: ...
input: ...
observation: ...

You MUST:
- Read and understand ALL previous steps carefully
- Track what has already been done
- NEVER repeat the same tool with the same input
- Continue reasoning from where you left off

{scratchpad}

==================================
USER QUERY
==================================

{user_query}

==================================
AVAILABLE TOOLS
==================================

- faiss_search → for knowledge, explanations
- calculator → for math calculations ONLY
- chat → ONLY for final user-friendly response OR greetings OR personal/casual conversation OR giving information
- whatsApp → open WhatsApp
- weather → get weather info
- web_search → internet search , ideas
- finish → ONLY when task is completely solved

==================================
MANDATORY ANTI-REPETITION CHECK
==================================

Before choosing ANY tool, you MUST:

1. Compare your intended action with ALL previous steps
2. Check if the SAME tool + SAME input was already used

If YES:
- DO NOT repeat it
- Choose a different tool OR move toward final answer

Repeating the same action is STRICTLY FORBIDDEN.

==================================
MULTI-TASK RULE (VERY IMPORTANT)
==================================

If the query contains multiple tasks:

1. Identify each task
2. Solve them ONE by ONE
3. Do NOT repeat completed tasks
4. When ALL tasks are complete → use finish

==================================
PERSONAL MEMORY RULE (VERY IMPORTANT)
==================================

If the user asks about:
- their name
- their city
- their preferences
- past conversation

→ You MUST answer using MEMORY
→ DO NOT use web_search or faiss_search

Examples:

User: what is my name  
→ finish using memory

User: where do I live  
→ finish using memory

==================================
REASONING LOOP
==================================

At each step:

1. Review the scratchpad
2. Decide what is already solved
3. Choose ONE best next action
4. Execute tool
5. Wait for observation
6. Continue until fully solved

==================================
IMPORTANT RULES
==================================

- If faiss_search returns NO_CONTEXT → NEVER use it again
- If enough information is already available → DO NOT call tools again
- Always make forward progress (never repeat useless steps)
- If all tasks are completed → immediately use "finish"
- Be efficient, but DO NOT skip necessary reasoning
-NEVER use faiss_search or web_search for casual talk, preferences,suggestions

==================================
STOP CONDITION (CRITICAL)
==================================

If the answer can be formed from existing observations:

→ IMMEDIATELY use "finish"  
→ DO NOT call any more tools  
→ DO NOT continue reasoning  

Return EXACTLY:

{{"thought": "final answer ready", "tool": "finish", "output": "..."}}

==================================
OUTPUT FORMAT (STRICT JSON ONLY)
==================================

You MUST return ONLY ONE JSON object.

Tool usage:
{{"thought": "short reasoning", "tool": "tool_name", "input": "tool input"}}

Final answer:
{{"thought": "final answer ready", "tool": "finish", "output": "final answer"}}

==================================
STRICT RULES
==================================

- Output MUST be valid JSON
- NO extra text before or after JSON
- NO markdown (no ``` )
- ONLY ONE JSON object
- MUST start with {{ and end with }}
- DO NOT explain anything outside JSON


==================================
NOW DECIDE NEXT STEP
==================================

Respond with ONLY your next decision as a single JSON object.

Do NOT repeat previous steps.
Do NOT explain anything.
Do NOT output anything except JSON.
"""

    messages = [{"role": "user", "content": decision_prompt}]

    answer = safe_calling_llm(messages, temperature=0.2, max_tokens=150)
    match = re.search(r"\{.*?\}", answer, re.DOTALL)

    if not match:
        print("NO JSON FOUND ❌☹️")
        print(answer)
        return {"tool": "finish", "output": "Model failed"}
    json_text = match.group()
    try:
        final_json = json.loads(json_text)
    except Exception as e:
        print("JSON PARSING FAILED 😭")
        print("ERROR : ", e)
        print("RAW OUTPUT : \n", answer)
        return {"tool": "finish", "output": "json paring failed"}

    return final_json
