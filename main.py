from fastapi import FastAPI

app = FastAPI(title="COSTLY", description="家計原価率管理アプリ")


@app.get("/")
def root():
    return {"message": "COSTLY API is running"}
