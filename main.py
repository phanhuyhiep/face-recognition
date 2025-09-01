import uvicorn

from configs.core_config import CoreSettings
from fastapi import FastAPI
from routes.user_routes import router as user_router
from routes.department_routes import router as department_router
from routes.employee_routes import router as employee_router

app = FastAPI(title="Face Recognition API", version="0.1.0")

port_project = CoreSettings.PORT
host_project = CoreSettings.HOST


app.include_router(user_router)
app.include_router(department_router)
app.include_router(employee_router)


@app.get("/")
async def root():
    return {"message": "Hello World from Face Recognition API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host = host_project, port = port_project, reload = True)