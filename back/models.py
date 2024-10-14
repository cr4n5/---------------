from pydantic import BaseModel

class RestartRequest(BaseModel):
    vote_obj: str

class LoginRequest(BaseModel):
    username: str
    password: str

class SetVoteInfoRequest(BaseModel):
    vote_obj: str
    list: list