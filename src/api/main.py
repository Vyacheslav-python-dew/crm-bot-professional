from fastapi import FastAPI

app = FastAPI(title="CRM Bot API")

@app.get("/")
async def root():
    return {"message": "API работает!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}