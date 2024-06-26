import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResp(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime.datetime
    owner_id: int 
    owner: UserResp

    class Config:
        from_attributes = True


class PostVote(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token : str
    token_type: str

class TokenData(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    id: Optional[str] = None 

class Vote(BaseModel):
    post_id: int
    dir: int

    @field_validator('dir')
    @classmethod
    def validate_dir(cls, value) -> int:
        if value not in (0, 1):
            raise ValueError("dir field must be either 0 or 1")
        return value
    