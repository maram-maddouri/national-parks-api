from fastapi import FastAPI
from app.routes import parks, species, users
from app.db import init_db

app = FastAPI()

app.include_router(parks.router)
app.include_router(species.router)
app.include_router(users.router)

@app.on_event("startup")
async def startup_event():
    init_db()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)