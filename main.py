import uvicorn

from configs.core_config import CoreSettings
from fastapi import FastAPI
from routes.user_routes import router as user_router

app = FastAPI(title="Face Recognition API", version="0.1.0")

port_project = CoreSettings.PORT
host_project = CoreSettings.HOST


app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "Hello World from Face Recognition API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host = host_project, port = port_project, reload = True)