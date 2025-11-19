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


# --- Seed Mock Data ---
@app.post("/seed")
def seed_mock_data():
    """Insert a set of mock users, listings, installers, leads, and quotes.
    Returns inserted ids for quick reference."""
    try:
        inserted: Dict[str, List[str]] = {
            "users": [],
            "listings": [],
            "installers": [],
            "leads": [],
            "quotes": [],
        }

        # Users
        users = [
            User(name="Alice Buyer", email="alice@example.com", role="buyer", city="Austin", state="TX"),
            User(name="Sam Seller", email="sam@sellsolar.co", role="seller", company="SellSolar", city="Phoenix", state="AZ"),
            User(name="Ivy Installer", email="ivy@brightinstalls.com", role="installer", company="Bright Installs", city="San Diego", state="CA"),
        ]
        for u in users:
            inserted["users"].append(create_document("user", u))

        # Listings
        listings = [
            Listing(title="450W Mono PERC Panel", description="High-efficiency Tier-1 module", product_type="panel", brand="SunPeak", wattage=450, price=219.0, images=["https://images.unsplash.com/photo-1509395176047-4a66953fd231?q=80&w=1200&auto=format&fit=crop"], seller_id=inserted["users"][1]),
            Listing(title="7kW Residential Package", description="Panels, inverter, racking, and monitoring", product_type="package", brand="SolarOne", price=11999.0, images=["https://images.unsplash.com/photo-1509395176047-4a66953fd231?q=80&w=1200&auto=format&fit=crop"], seller_id=inserted["users"][1]),
            Listing(title="Hybrid Inverter 6kW", description="Battery-ready hybrid inverter", product_type="inverter", brand="VoltMax", price=2499.0, images=["https://images.unsplash.com/photo-1581092808360-9a3b0c6a2831?q=80&w=1200&auto=format&fit=crop"], seller_id=inserted["users"][1]),
        ]
        for l in listings:
            inserted["listings"].append(create_document("listing", l))

        # Installers
        installers = [
            Installer(user_id=inserted["users"][2], services=["residential", "battery"], areas=["San Diego", "LA"], certifications=["NABCEP"], rating=4.8),
            Installer(user_id=inserted["users"][2], services=["commercial"], areas=["Orange County"], certifications=["NABCEP"], rating=4.6),
        ]
        for ins in installers:
            inserted["installers"].append(create_document("installer", ins))

        # Leads
        leads = [
            Leadrequest(buyer_name="Alice Buyer", buyer_email="alice@example.com", city="Austin", state="TX", avg_monthly_bill_usd=165.0, desired_system_size_kw=6.5, notes="South-facing roof, minimal shade"),
            Leadrequest(buyer_name="Bob Homeowner", buyer_email="bob@home.com", city="San Jose", state="CA", avg_monthly_bill_usd=210.0, desired_system_size_kw=8.0),
        ]
        for ld in leads:
            inserted["leads"].append(create_document("leadrequest", ld))

        # Quotes
        quotes = [
            Quote(lead_id=inserted["leads"][0], installer_id=inserted["users"][2], price_usd=15250.0, timeline_weeks=6, warranty_years=25, message="Includes 7.2kW array with monitoring", status="sent"),
            Quote(lead_id=inserted["leads"][0], installer_id=inserted["users"][2], price_usd=13999.0, timeline_weeks=5, warranty_years=20, message="Budget option, same output", status="sent"),
            Quote(lead_id=inserted["leads"][1], installer_id=inserted["users"][2], price_usd=17200.0, timeline_weeks=7, warranty_years=25, message="8kW premium components", status="sent"),
        ]
        for q in quotes:
            inserted["quotes"].append(create_document("quote", q))

        return {"inserted": inserted}
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
