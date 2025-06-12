from fastapi import FastAPI,Request
from app.core.database import Base, engine
from app.auth.routes import router as auth_router
from app.products.routes import router as products_router
from app.products.public_products_routes import router as public_products_router
from app.orders.routes import router as orders_router
from app.cart.routes import router as cart_router
from app.checkout.routes import router as checkout_router

##exception handling
import logging
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

##logging middleware
import traceback
from app.middlewares.logging_middleware import LoggingMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/log_file.log"),  
        logging.StreamHandler()
    ]
)


Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce Backend System Using FastAPI")

app.add_middleware(LoggingMiddleware)

app.include_router(auth_router)
app.include_router(products_router)
app.include_router(public_products_router)
app.include_router(orders_router)
app.include_router(cart_router)
app.include_router(checkout_router)



@app.get("/")
def root():
    return {"message": " E-commerce Backend System "}


##exceptional handling
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logging.warning(f" HTTPException at {request.url.path} | Status: {exc.status_code} | Detail: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "message": exc.detail, "code": exc.status_code},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.warning(f" Validation error at {request.url.path} | Errors: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"error": True, "message": str(exc), "code": 422},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f" Unhandled Exception at {request.url.path}: {repr(exc)}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={"error": True, "message": "Internal Server Error", "code": 500},
    )