from fastapi import FastAPI
from routers import url, analytics, redirect, services
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(url.router, prefix="/url", tags=["URL Shortening"])
# app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(services.router, tags=["Services"])
app.include_router(redirect.router, tags=["Redirect"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
