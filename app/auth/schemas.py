from pydantic import BaseModel, EmailStr, validator
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

    ## create custom strong password validator
    @validator('password')
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

    @validator('new_password')
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