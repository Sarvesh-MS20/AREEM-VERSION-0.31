from db.db_ops import create_user,save_memory
from agent.runner import run_agent
from API.schemas import ChatRequest,ChatResponse
user_id = create_user("sarvesh")
from fastapi import APIRouter,HTTPException
from Guadrails.input_guardrails import is_query_safe
from Guadrails.output_guardrails import clean_output
import asyncio

router = APIRouter()

@router.post("/chat",response_model = ChatResponse)
async def chatt(request:ChatRequest):
    try:
        query = request.query

        user_id = request.user_id

        if not query:
            return ChatResponse(response = "query cannot be empty" )

        if not is_query_safe(query):
            raise HTTPException(status_code = 400 , detail = "Unsafe input")

        save_memory(user_id,"user",query)

        '''answer = run_agent(query,user_id)'''

        answer = await asyncio.to_thread(run_agent,query , user_id)

        if not answer :
            return "Something went wrong can't be answer 😜"

        answer = clean_output(answer)
        save_memory(user_id, "AI",str(answer))
        return ChatResponse(response = str(answer))
    except Exception as e:
        raise HTTPException(status_code = 500 , detail = str(e))




