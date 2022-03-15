from fastapi import FastAPI

from stranger_danger.api.app.routers import fences

app = FastAPI()


app.include_router(fences.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
