from fastapi import FastAPI

from stranger_danger.api.app.routers import pentagon_fences

app = FastAPI()


app.include_router(pentagon_fences.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
