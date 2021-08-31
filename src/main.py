from fastapi import FastAPI
import sqlite3 as sl
from src.get_data import FbDataLoader
app = FastAPI()

#Database connect
db = sl.connect('../my-test.db')

#root route
@app.get("/")
async def root():
    return {"message": "Hello"}

#Heath check route
@app.get("/PING")
async def health_check():
    return {"message": "PONG"}

#route to collect post data and add it to the database from facebook public profile or page
@app.get("/{profile}")
async def fb_posts(profile):
    url = f'https://www.facebook.com/{profile}'
    fb_loader = FbDataLoader(url, db)
    fb_loader.posts_to_db()
    #checking data
    if fb_loader.get_data() is not None:
        return {"message": f"Posts from {url} added to the database Successfully"}
    else:
        return {"message": f"ERROR to load {url}"}
