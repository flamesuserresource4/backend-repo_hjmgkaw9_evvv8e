import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List

from database import db, create_document, get_documents
from schemas import User, Listing, Installer, Leadrequest, Quote

app = FastAPI(title="Solar Marketplace API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Solar Marketplace API running"}


# --- Schema Introspection for tools ---
@app.get("/schema")
def get_schema():
    return {
        "collections": [
            "user",
            "listing",
            "installer",
            "leadrequest",
            "quote",
        ]
    }


# --- Users ---
@app.post("/users")
def create_user(user: User):
    try:
        new_id = create_document("user", user)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users")
def list_users():
    try:
        docs = get_documents("user", {})
        for d in docs:
            d["_id"] = str(d["_id"])  # stringify ObjectId
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Listings ---
@app.post("/listings")
def create_listing(listing: Listing):
    try:
        new_id = create_document("listing", listing)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/listings")
def list_listings():
    try:
        docs = get_documents("listing", {})
        for d in docs:
            d["_id"] = str(d["_id"])  # stringify ObjectId
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Installers ---
@app.post("/installers")
def create_installer(installer: Installer):
    try:
        new_id = create_document("installer", installer)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/installers")
def list_installers():
    try:
        docs = get_documents("installer", {})
        for d in docs:
            d["_id"] = str(d["_id"])  # stringify ObjectId
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Leads ---
@app.post("/leads")
def create_lead(lead: Leadrequest):
    try:
        new_id = create_document("leadrequest", lead)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/leads")
def list_leads():
    try:
        docs = get_documents("leadrequest", {})
        for d in docs:
            d["_id"] = str(d["_id"])  # stringify ObjectId
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Quotes ---
@app.post("/quotes")
def create_quote(quote: Quote):
    try:
        new_id = create_document("quote", quote)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/quotes")
def list_quotes():
    try:
        docs = get_documents("quote", {})
        for d in docs:
            d["_id"] = str(d["_id"])  # stringify ObjectId
        return docs
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
        "collections": [],
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, "name") else "✅ Connected"
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

    import os as _os
    response["database_url"] = "✅ Set" if _os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if _os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
