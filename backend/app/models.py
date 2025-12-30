from datetime import date, datetime
from enum import Enum
from typing import Optional, List

from sqlmodel import Field, SQLModel


class ShipmentStatus(str, Enum):
    CREATED = "created"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELED = "canceled"


class ShipmentBase(SQLModel):
    tracking_number: str = Field(index=True, max_length=64, sa_column_kwargs={"unique": True})
    shipper: str = Field(max_length=120)
    consignee: str = Field(max_length=120)
    origin: str = Field(max_length=160)
    destination: str = Field(max_length=160)
    carrier: Optional[str] = Field(default=None, max_length=120)
    status: ShipmentStatus = Field(default=ShipmentStatus.CREATED)
    pieces: int = Field(ge=1, default=1)
    weight_kg: float = Field(ge=0, default=0)
    cost: float = Field(ge=0, default=0)
    pickup_date: Optional[date] = Field(default=None)
    expected_delivery: Optional[date] = Field(default=None)
    delivered_at: Optional[datetime] = Field(default=None)
    notes: Optional[str] = Field(default=None, max_length=800)


class Shipment(ShipmentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class ShipmentCreate(ShipmentBase):
    pass


class ShipmentUpdate(SQLModel):
    tracking_number: Optional[str] = Field(default=None, max_length=64)
    shipper: Optional[str] = Field(default=None, max_length=120)
    consignee: Optional[str] = Field(default=None, max_length=120)
    origin: Optional[str] = Field(default=None, max_length=160)
    destination: Optional[str] = Field(default=None, max_length=160)
    carrier: Optional[str] = Field(default=None, max_length=120)
    status: Optional[ShipmentStatus] = Field(default=None)
    pieces: Optional[int] = Field(default=None, ge=1)
    weight_kg: Optional[float] = Field(default=None, ge=0)
    cost: Optional[float] = Field(default=None, ge=0)
    pickup_date: Optional[date] = Field(default=None)
    expected_delivery: Optional[date] = Field(default=None)
    delivered_at: Optional[datetime] = Field(default=None)
    notes: Optional[str] = Field(default=None, max_length=800)


class ShipmentList(SQLModel):
    total: int
    items: List[Shipment]
