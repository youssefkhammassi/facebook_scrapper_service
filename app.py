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
    return uvicorn.run("app:app", host=mira_tms_config.HOST, port=mira_tms_config.PORT)


if __name__ == "__main__":
    run()