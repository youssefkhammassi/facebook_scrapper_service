import os

import uvicorn
from fastapi import FastAPI
app = FastAPI()

#root route
@app.get("/")
async def root():
    return {"message": "Hello"}

#Heath check route
@app.get("/PING")
async def health_check():
    return {"message": "PONG"}

def run():
    return uvicorn.run("app:app", host='0.0.0.0', port=os.getenv('PORT', 8088))


if __name__ == "__main__":
    run()