#agent/runner.py

from memory.long_term import smart_memory_storage_decider, smart_memory_extractor, clean_memory
from memory.long_term import load_memory
from db.db_ops import save_memory
from agent.planner import planner
from agent.decision import decide_agent
from agent.critic import critic_agent
from agent.executor import execute_tools

# -------------------------------------------------------------------------------------------
def run_agent(query,user_id):
    # loading chat
    memory = load_memory(user_id)  # loading the memory

    # memory pipeline
    if smart_memory_storage_decider(query):
        memory = smart_memory_extractor(query, memory)  # calling the extraction function
        memory = clean_memory(memory)
        for k,v in memory.items():
            save_memory(user_id,k,v)  # save after update



    # ------------------------------------------------------------------------------------------
    # 🔥 DIRECT MEMORY ANSWERS
    if "name" in query.lower() and "my" in query.lower():
        if "name" in memory:
            return f"Your name is {memory['name']}"

    if "where do i live" in query.lower() or "my city" in query.lower():
        if "city" in memory:
            return f"You live in {memory['city']}"
    # -------------------------------------------------------------------------------------------

    # planner

    plan = planner(query)
    tasks = plan.get("tasks")

    # plan generated
    for t in tasks:
        print(t, "\n")

    final_answer = []

    for task in tasks:
        step_query = task.get("input", query)
        scratchpad = ""
        used_calls = set()
        collected = []
        context_memory = ""
        used_faiss = False  # to keep track of the usage of faiss

        critic_retry = 0

        for i in range(7):
            decision = decide_agent(step_query, scratchpad)
            print("=====RAW DECISION======")
            print(decision)
            print("=======================")

            if decision is None:
                print("still broken : ", decision)
                return "ERROR : INVALID JSON"

            # IF DECISION IS N0T NONE
            tool = decision.get("tool", "")

            # tool fallback
            allowed_tools = ["faiss_search", "calculator", "web_search", "whatsApp", "chat","finish"]
            if tool not in allowed_tools:
                return "Invalid tool selected"

            thought = decision.get("thought", "")

            tool_input = decision.get("input", "").strip()
            # tool input fallback
            if not tool_input:
                tool = "chat"
                tool_input = query

            # --------------------------------------------------
            #           tool execution
            # --------------------------------------------------
            if tool == "finish":
                final_answer.append(decision.get("output", ""))
                final_text = "\n".join(final_answer)
                critic = critic_agent(query, final_text)

                # critic check
                print("critic 🧐 : ", critic)

                # if critic is wrong

                if critic.get("verdict") == "wrong":
                    critic_retry += 1
                    if critic_retry >= 2:
                        print("critic failed too many times , anyway returning the answer")
                        return final_answer

                    # adding feedback into the scratchpad
                    scratchpad += f"\n CRITIC FEEDBACK : {critic.get('reason', 'improve answer')}\n"
                    continue  # wrong tool so go to next loop

                return final_answer

            if not final_answer :
                return "Sorry i could'nt able to process the result..."

            # to check the same input and tool has already been used in scratchpad

            logs = (tool, tool_input.strip().lower())

            if logs in used_calls:
                scratchpad += f"""
                Step {i + 1}:
                thought: repeated action blocked
                tool: None
                input: None
                observation: You already used {tool} with {tool_input}.Move to finish
                """

                continue

            used_calls.add(logs)

            result, used_faiss, context_memory = execute_tools(
            tool, tool_input, memory, user_id, context_memory, used_faiss, scratchpad
            )
            collected.append(f"{tool}({tool_input})-->{result}")

            if tool == "faiss_search" and result == "NO_CONTEXT":
                scratchpad += "\n FAISS FAILED , DO NOT USE AGAIN\n"

            scratchpad += f"""
                Step {i + 1}:
                thought: {thought}
                tool: {tool}
                input: {tool_input}
                observation: {result}
                """
            # if we reach max step without a proper "finish" try to build an answer with what we got so far
        if collected:
            return "Look at here what we got : \n" + "\n".join(collected)

        return "agent stopped"






