from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class VehicleSpec(BaseModel):
    plate: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    version: Optional[str] = None
    engine: Optional[str] = None
    fuel: Optional[str] = None
    vin: Optional[str] = None

    model_config = {"extra": "forbid"}


class Location(BaseModel):
    cep: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None

    model_config = {"extra": "allow"}  # permitimos campos extras (GPS do WhatsApp)


class Contact(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    whatsappId: Optional[str] = None

    model_config = {"extra": "allow"}


Urgency = Literal["ALTA", "NORMAL", "ORCAMENTO"]
Category = Literal[
    "Freios", "Suspensão", "Motor", "Elétrica", "Transmissão", "Arrefecimento", "Outros"
]


class PartRequestCreate(BaseModel):
    category: Category
    subcategory: Optional[str] = None
    vehicle: VehicleSpec
    symptoms: List[str] = Field(default_factory=list)
    notes: Optional[str] = None
    attachments: List[str] = Field(default_factory=list)
    urgency: Urgency
    location: Optional[Location] = None
    preferredBrands: List[str] = Field(default_factory=list)
    maxBudget: Optional[float] = None
    consentToShare: bool = True
    contact: Optional[Contact] = None

    model_config = {"extra": "forbid"}
