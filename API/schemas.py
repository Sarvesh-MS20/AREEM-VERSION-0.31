from pydantic import BaseModel,field_validator

class ChatRequest(BaseModel):
    query:str
    user_id : int

    #input guardrails
    @field_validator("query")
    def validate_query(cls,v):
        if len(v)>500:
            raise ValueError("Query is very long🥱")
        if v.strip() = "":
            raise ValueError("Query is empty 😝")

        return v






class ChatResponse(BaseModel):
    response:str