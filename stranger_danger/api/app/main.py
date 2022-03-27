from fastapi import FastAPI

from stranger_danger.api.app.routers import areas, detector, email, fences, users

app = FastAPI()


app.include_router(areas.router)
app.include_router(fences.router)
app.include_router(detector.router)
app.include_router(users.router)
app.include_router(email.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
