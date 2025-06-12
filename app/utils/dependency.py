
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.auth import models, utils
from app.core.database import SessionLocal

bearer_scheme = HTTPBearer()  

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get Current User from JWT
def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token.credentials, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])
        email = payload.get("sub")
        role = payload.get("role")
        user = db.query(models.User).filter_by(email=email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token error")

# Admin-only dependency
def require_admin(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return current_user

## User-only dependency
def require_user(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "user":
        raise HTTPException(status_code=403, detail="Users only")
    return current_user
