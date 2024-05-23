from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from api import auth, heartbeat, setting, user
from otp import trace, tracer

app = FastAPI()

app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(heartbeat.router, prefix="/api")
app.include_router(setting.router, prefix="/api")
# app.include_router(me.router, prefix="/api")

origins = [
    "*",
]

methods = [
    "DELETE",
    "GET",
    "POST",
    "PUT",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=["*"],
)


@trace("connect_database", test_attr="test_value")
# async def connect_db():
# try:
#     await deps.get_db()
# except Exception as e:
#     print(e)


@app.on_event("startup")
async def startup():
    with tracer.start_as_current_span("startup_span") as span:
        print("startup")
    # await connect_db()
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)


# @app.on_event("shutdown")
# async def shutdown():
#     if database.is_connected:
#         await database.disconnect()

FastAPIInstrumentor.instrument_app(app)
