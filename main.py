
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import uvicorn
from fastapi import FastAPI
from starlette.responses import JSONResponse
from core.environment import settings
from metadata.tags import Tags
from routers import (employee_router,
                     department_router,
                     device_router,
                     event_router,
                     auth_router,
                     user_router)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    openapi_tags=Tags,
)

# Add Routers
app.include_router(employee_router)
app.include_router(department_router)
app.include_router(device_router)
app.include_router(event_router)
app.include_router(user_router)
app.include_router(auth_router)


@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content=jsonable_encoder({"code": 500, "msg": "Internal Server Error"}))


@app.get("/", include_in_schema=False)
def check_health() -> JSONResponse:
    return JSONResponse({"message": "It works!!"})


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

