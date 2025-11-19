"""
Database Schemas for Solar Marketplace

Each Pydantic model represents a MongoDB collection. The collection name is the
lowercase of the class name (e.g., User -> "user").

These schemas are used for validation and are also surfaced via the /schema
endpoint so tools can understand your data model.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Literal

# ---------- Core Users ----------
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    role: Literal["buyer", "seller", "installer"] = Field(
        ..., description="User role in the marketplace"
    )
    company: Optional[str] = Field(None, description="Company name if applicable")
    city: Optional[str] = Field(None, description="City or locality")
    state: Optional[str] = Field(None, description="State or region")
    is_active: bool = Field(True, description="Whether user is active")

# ---------- Product Listings ----------
class Listing(BaseModel):
    title: str = Field(..., description="Listing title")
    description: Optional[str] = Field(None, description="Description of the product/package")
    product_type: Literal["panel", "inverter", "battery", "package"] = Field(
        ..., description="Type of product"
    )
    brand: Optional[str] = Field(None, description="Brand name")
    wattage: Optional[int] = Field(None, ge=0, description="Panel wattage if applicable")
    price: float = Field(..., ge=0, description="Price in USD")
    seller_id: Optional[str] = Field(None, description="Seller user id (string)")
    images: Optional[List[str]] = Field(default=None, description="Image URLs")
    in_stock: bool = Field(True, description="Whether product is available")

# ---------- Installer Profiles ----------
class Installer(BaseModel):
    user_id: str = Field(..., description="Linked user id for installer")
    services: List[str] = Field(default_factory=list, description="Services offered")
    areas: List[str] = Field(default_factory=list, description="Service areas (cities/regions)")
    certifications: List[str] = Field(default_factory=list, description="Certifications")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Average rating")

# ---------- Buyer Lead Requests ----------
class Leadrequest(BaseModel):
    buyer_name: str = Field(..., description="Buyer name")
    buyer_email: str = Field(..., description="Buyer email")
    buyer_phone: Optional[str] = Field(None, description="Buyer phone")
    city: Optional[str] = Field(None, description="City or locality")
    state: Optional[str] = Field(None, description="State or region")
    roof_type: Optional[str] = Field(None, description="Roof type (tile/metal/flat)")
    avg_monthly_bill_usd: Optional[float] = Field(None, ge=0, description="Average monthly electricity bill")
    desired_system_size_kw: Optional[float] = Field(None, ge=0, description="Desired system size in kW")
    notes: Optional[str] = Field(None, description="Additional notes")

# ---------- Quotes from Installers ----------
class Quote(BaseModel):
    lead_id: str = Field(..., description="Lead request id")
    installer_id: str = Field(..., description="Installer user id")
    price_usd: float = Field(..., ge=0, description="Quoted total price in USD")
    timeline_weeks: Optional[int] = Field(None, ge=0, description="Estimated install timeline in weeks")
    warranty_years: Optional[int] = Field(None, ge=0, description="Warranty in years")
    message: Optional[str] = Field(None, description="Quote message/details")
    status: Literal["sent", "accepted", "rejected"] = Field("sent", description="Quote status")
