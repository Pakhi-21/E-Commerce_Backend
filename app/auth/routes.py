from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.auth import schemas, utils, models, email_utils
from app.core.database import SessionLocal
from jose import JWTError, jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from app.utils.dependency import get_db
import logging


logger = logging.getLogger("ecommerce_logger")


router = APIRouter(prefix="/auth", tags=["Auth"])
bearer_scheme = HTTPBearer()  

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", status_code=201)
def signup(data: schemas.Signup, db: Session = Depends(get_db)):
    user=db.query(models.User).filter_by(email=data.email).first()

    if (user):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    hashed_pw = utils.hash_password(data.password)
    user = models.User(name=data.name, email=data.email, hashed_password=hashed_pw, role=data.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created successfully"}

@router.post("/signin", response_model=schemas.Token)
def signin(data: schemas.Signin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(email=data.email).first()

    if not user or not utils.verify_password(data.password, user.hashed_password):
        logger.warning(f"Failed login attempt for email: {data.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    logger.info(f" Successful login for email: {data.email}")
    payload = {"sub": user.email, "role": user.role}
    access_token = utils.create_access_token(payload)
    refresh_token = utils.create_refresh_token(payload)

    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/forgot-password")
def forgot_password(data: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)):

    user = db.query(models.User).filter_by(email=data.email).first()
    if (not user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Email not found. Please check and try again.")
    
    ##reset_token = utils.create_password_reset_token(user.email)
    ##replace
    reset_token = utils.create_and_store_password_reset_token(db, user)

    ## Send the reset token via mail us SMTP
    email_utils.send_reset_email(user.email, reset_token)

    return {"message": "If the email is registered, a reset token has been sent to your email."}

# @router.post("/reset-password")
# def reset_password(data: schemas.ResetPasswordRequest, db: Session = Depends(get_db)):
#     email = utils.verify_password_reset_token(data.token)
#     if email is None:
#         raise HTTPException(status_code=400, detail="Invalid or expired token")
#     user = db.query(models.User).filter_by(email=email).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     hashed_pw = utils.hash_password(data.new_password)
#     user.hashed_password = hashed_pw
#     db.commit()
#     return {"message": "Password reset successful"}

#replace
@router.post("/reset-password")
def reset_password(data: schemas.ResetPasswordRequest, db: Session = Depends(get_db)):
    db_token = db.query(models.PasswordResetToken).filter_by(token=data.token).first()

    if not db_token:
        raise HTTPException(status_code=400, detail="Invalid token")

    if db_token.used:
        raise HTTPException(status_code=400, detail="Token already used")

    if db_token.expiration_time.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Token expired")

    user = db_token.user
    hashed_pw = utils.hash_password(data.new_password)
    user.hashed_password = hashed_pw

    # Mark token as used
    db_token.used = True
    db.commit()

    return {"message": "Password reset successful"}

@router.post("/refresh-token", response_model=schemas.Token)
def refresh_token(data: schemas.RefreshTokenRequest):
    try:
        payload = utils.decode_token(data.refresh_token)
        email = payload.get("sub")
        role = payload.get("role")

        new_access_token = utils.create_access_token({"sub": email, "role": role})
        new_refresh_token = utils.create_refresh_token({"sub": email, "role": role})

        return {"access_token": new_access_token, "refresh_token": new_refresh_token}
    
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


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