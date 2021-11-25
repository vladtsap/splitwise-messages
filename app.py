from fastapi import FastAPI, Response

import monobank
import splitwise
from config import engine, Base

app = FastAPI()

app.include_router(splitwise.router)
app.include_router(monobank.router)


@app.get('/')
async def ping():
    return Response()


Base.metadata.create_all(bind=engine)
