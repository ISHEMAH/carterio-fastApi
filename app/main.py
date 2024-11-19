from fastapi import FastAPI
from app.routers import users, roles

app = FastAPI()

@app.on_event("startup")
def startup():
    from app.database import Base, engine
    Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(roles.router, prefix="/api/roles", tags=["roles"])
