from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from helpers import response_parser
from api import routers

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def custom_exception_handler(request: Request, call_next):
    try:
        return await call_next(request)

    except Exception as e:
        raise response_parser.generate_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"Internal server error: {e.args}",
            success=False,
        )


app.include_router(routers.router, prefix=settings.API_V1_PREFIX)
