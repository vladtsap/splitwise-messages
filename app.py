from fastapi import FastAPI, Response

import splitwise

app = FastAPI()

app.include_router(splitwise.router)


@app.get('/')
async def index():
    return Response()
