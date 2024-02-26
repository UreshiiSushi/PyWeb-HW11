from fastapi import FastAPI

from contacts.routes import contacts

app = FastAPI()

app.include_router(contacts.router, prefix="/contacts")


@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}
