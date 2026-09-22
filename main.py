from fastapi import FastAPI
from routers import expenses

app = FastAPI(title="COSTLY", description="家計原価率管理アプリ")

app.include_router(expenses.router)


@app.get("/")
def root():
    return {"message": "COSTLY API is running"}
