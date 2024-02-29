from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from otp import trace
from api import user, auth, me

from api import auth, me, user
from bootstrap.db import Base, database, engine

app = FastAPI()
app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(me.router, prefix="/api")

origins = [
    "http://localhost:5173",
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

@trace("connect_database",test_attr="test_value")
async def connect_db():
    try:
        await database.connect()
    except Exception as e:
        print(e)

@app.on_event("startup")
async def startup():
    init_tracer()
    await connect_db()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
