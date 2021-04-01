from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello"}

@app.post("/")
def root():
    return {"message": "Hello World"}