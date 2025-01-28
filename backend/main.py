from fastapi import FastAPI
from routers import url, analytics, redirect

app = FastAPI()

app.include_router(url.router, prefix="/url", tags=["URL Shortening"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(redirect.router, tags=["Redirect"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)