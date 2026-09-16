from fastapi import FastAPI
from app.routers import applications, companies

app = FastAPI(title="Job Application Tracker")

app.include_router(applications.router)
app.include_router(companies.router)

@app.get("/health")
def health():
    return {"status": "ok"}