from pydantic import BaseModel, EmailStr, field_validator
from enum import Enum
import re

class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"

class Signup(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: RoleEnum = RoleEnum.user
    
    #name validator
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty")
        if not (2 <= len(v) <= 100):
            raise ValueError("Name must be between 2 and 100 characters long")
        return v

    ## create custom strong password validator
    @field_validator('password')
    @classmethod
    def strong_password(cls, v):
        pattern = re.compile(
            r'^(?=.*[a-z])'      
            r'(?=.*[A-Z])'       
            r'(?=.*\d)'          
            r'(?=.*[!@#$%^&*(),.?":{}|<>])'  
            r'.{8,}$'            
        )
        if not pattern.match(v):
            raise ValueError('Password must be at least 8 characters long and include uppercase, lowercase, digit, and special character')
        return v

class Signin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

    @field_validator('new_password')
    @classmethod
    def strong_password(cls, v):
        pattern = re.compile(
            r'^(?=.*[a-z])'      
            r'(?=.*[A-Z])'       
            r'(?=.*\d)'          
            r'(?=.*[!@#$%^&*(),.?":{}|<>])'  
            r'.{8,}$'            
        )
        if not pattern.match(v):
            raise ValueError('Password must be at least 8 characters long and include uppercase, lowercase, digit, and special character')
        return v

    
class RefreshTokenRequest(BaseModel):
    refresh_token: str