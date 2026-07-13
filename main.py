from fastapi import FastAPI

from app.database.connection import init_db, test_db_connection
from app.route.user_route import router as user_router
from app.core.config import settings

app = FastAPI(
    title="RAG Project API",
    version="1.0.0",
    description="Postman-ready user registration API.",
)


@app.get("/")
def root() -> dict:
    return {"message": "RAG Project API is running"}


@app.get("/health")
def health() -> dict:
    return {
        "database_connection": test_db_connection(),
    }


@app.on_event("startup")
def startup_event() -> None:
    if test_db_connection():
        init_db()


app.include_router(user_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=False)