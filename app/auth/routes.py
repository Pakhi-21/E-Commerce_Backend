from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth import schemas, utils, models, email_utils
from app.core.database import SessionLocal
from jose import JWTError, jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from app.utils.dependency import get_db, get_current_user, require_admin
from jose.exceptions import JWTError as JoseJWTError 
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

#create user & admin
@router.post("/signup", status_code=201)
def signup(data: schemas.Signup, db: Session = Depends(get_db)):
    try:
        user=db.query(models.User).filter_by(email=data.email).first()

        if (user):
            raise HTTPException(status_code=400, detail="Email already exists")
        
        hashed_pw = utils.hash_password(data.password)
        user = models.User(name=data.name, email=data.email, hashed_password=hashed_pw, role=data.role)
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"User created successfully: {data.email}")
        return {"message": "User created successfully"}
    
    except HTTPException as http_exc:
         raise http_exc
     
    except Exception as e:
        db.rollback()
        logger.error(f"Error in signup: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

##login user & admin
@router.post("/signin", response_model=schemas.Token)
def signin(data: schemas.Signin, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter_by(email=data.email).first()

        if not user or not utils.verify_password(data.password, user.hashed_password):
            logger.warning(f"Failed login attempt for email: {data.email}")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        logger.info(f" Successful login for email: {data.email}")
        payload = {"sub": user.email, "role": user.role}
        access_token = utils.create_access_token(payload)
        refresh_token = utils.create_refresh_token(payload)

        return {"access_token": access_token, "refresh_token": refresh_token}
    
    except HTTPException as http_exc:
         raise http_exc
     
    except Exception as e:
        logger.error(f"Error in signin: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

## forget password    
@router.post("/forgot-password")
def forgot_password(data: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter_by(email=data.email).first()
        if (not user):
            logger.warning("Email not found for password reset")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Email not found. Please check and try again.")
        
        reset_token = utils.create_and_store_password_reset_token(db, user)

        ## Send the reset token via mail us SMTP
        email_utils.send_reset_email(user.email, reset_token)
        logger.info("Reset token sent to email") 
        return {"message": "Reset token mail send Successfully."}
    
    except HTTPException as http_exc:
         raise http_exc
     
    except Exception as e:
        db.rollback(f"Error in Forget password: {str(e)}")
        logger.error()
        raise HTTPException(status_code=500, detail="Internal Server Error")


# reset password 
@router.post("/reset-password")
def reset_password(data: schemas.ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        db_token = db.query(models.PasswordResetToken).filter_by(token=data.token).first()

        if not db_token:
            logger.warning("Invalid reset token used")
            raise HTTPException(status_code=400, detail="Invalid token")

        if db_token.used:
            logger.warning("Reset token already used")
            raise HTTPException(status_code=400, detail="Token already used")

        if db_token.expiration_time.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            logger.warning("Reset token expired")
            raise HTTPException(status_code=400, detail="Token expired")

        user = db_token.user
        hashed_pw = utils.hash_password(data.new_password)
        user.hashed_password = hashed_pw

        # Mark token as used
        db_token.used = True
        db.commit()
        logger.info("Password reset successfully")
        return {"message": "Password reset successful"}
    
    except HTTPException as http_exc:
         raise http_exc
      
    except Exception as e:
        db.rollback()
        logger.error(f"Error in reset-password: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

## refresh token
@router.post("/refresh-token", response_model=schemas.Token)
def refresh_token(data: schemas.RefreshTokenRequest):
    try:
        payload = utils.decode_token(data.refresh_token)

        if payload is None or not isinstance(payload, dict):
            logger.warning("Invalid refresh token: payload is None or invalid format")
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        email = payload.get("sub")
        role = payload.get("role")

        logger.info("Refresh token")  
        new_access_token = utils.create_access_token({"sub": email, "role": role})
        new_refresh_token = utils.create_refresh_token({"sub": email, "role": role})

        return {"access_token": new_access_token, "refresh_token": new_refresh_token}
    
    except HTTPException as http_exc:
         raise http_exc
    
    except Exception as e:
        logger.error(f"Error in refresh-token: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

