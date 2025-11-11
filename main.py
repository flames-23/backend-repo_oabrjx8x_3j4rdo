import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from database import create_document, get_documents, db
from schemas import Event, Announcement, ContactMessage, Officer

app = FastAPI(title="Math Club API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Math Club API is running"}

# Public endpoints
@app.get("/api/events")
def list_events(limit: int = 50):
    try:
        events = get_documents("event", {}, limit)
        for e in events:
            e["_id"] = str(e["_id"])
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/announcements")
def list_announcements(limit: int = 10):
    try:
        anns = get_documents("announcement", {"visible": True}, limit)
        for a in anns:
            a["_id"] = str(a["_id"])
        return anns
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ContactResponse(BaseModel):
    status: str

@app.post("/api/contact", response_model=ContactResponse)
def submit_contact(msg: ContactMessage):
    try:
        create_document("contactmessage", msg)
        return {"status": "received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
