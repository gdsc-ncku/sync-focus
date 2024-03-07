import time

from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse, RedirectResponse

from exception.exception import BaseAPIException

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(BaseAPIException)
async def http_exception_handler(request: Request, exception: BaseAPIException):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "message": exception.message,
            "detail": exception.detail,
            "error_code": exception.error_code,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exception: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message": "Validation Error",
            "detail": exception.errors(),
        },
    )


@app.middleware("https")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/", status_code=status.HTTP_307_TEMPORARY_REDIRECT, include_in_schema=False)
async def root_endpoint():
    return RedirectResponse(url="/redoc")


# app.include_router(
#     container_router,
#     prefix="/containers",
#     tags=["containers"],
# )

# app.include_router(
#     tenant_router,
#     prefix="/tenants",
#     tags=["tenants"],
# )
