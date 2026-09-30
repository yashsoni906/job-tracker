from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import applications, companies, contacts, analytics

app = FastAPI(title="Job Application Tracker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(applications.router)
app.include_router(companies.router)
app.include_router(contacts.router)
app.include_router(analytics.router)

@app.get("/health")
def health():
    return {"status": "ok"}