from typing import Annotated
from fastapi import FastAPI, Depends

app = FastAPI(
    title='Trading App'  # add name for our app
)


async def common_parameters(q: str | None = None, skip: int = 0):
    return {"q": q, "skip": skip}


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
