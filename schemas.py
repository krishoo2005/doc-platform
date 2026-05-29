from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str   

class ChatRequest(BaseModel):
    document_id: int
    question: str         