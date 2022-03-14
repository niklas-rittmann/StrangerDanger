from fastapi import FastAPI

from stranger_danger.api.app.routers import (
    circular_fences,
    pentagon_fences,
    rectangular_fences,
)

app = FastAPI()


app.include_router(rectangular_fences.router)
app.include_router(circular_fences.router)
app.include_router(pentagon_fences.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
