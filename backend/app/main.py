from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from sqlalchemy import func

from .database import get_session, init_db
from .models import Shipment, ShipmentCreate, ShipmentUpdate, ShipmentList

app = FastAPI(title="TMS API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/shipments", response_model=ShipmentList)
def list_shipments(
    limit: int = 10,
    offset: int = 0,
    session: Session = Depends(get_session),
) -> ShipmentList:
    limit = max(1, min(limit, 100))
    offset = max(0, offset)
    total = session.exec(select(func.count()).select_from(Shipment)).one()
    statement = select(Shipment).order_by(Shipment.id.desc()).offset(offset).limit(limit)
    items = session.exec(statement).all()
    return ShipmentList(total=total, items=items)


@app.post("/shipments", response_model=Shipment, status_code=status.HTTP_201_CREATED)
def create_shipment(payload: ShipmentCreate, session: Session = Depends(get_session)) -> Shipment:
    shipment = Shipment.from_orm(payload)
    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    return shipment


@app.get("/shipments/{shipment_id}", response_model=Shipment)
def get_shipment(shipment_id: int, session: Session = Depends(get_session)) -> Shipment:
    shipment = session.get(Shipment, shipment_id)
    if not shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    return shipment


@app.put("/shipments/{shipment_id}", response_model=Shipment)
def update_shipment(shipment_id: int, payload: ShipmentUpdate, session: Session = Depends(get_session)) -> Shipment:
    shipment = session.get(Shipment, shipment_id)
    if not shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")

    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(shipment, key, value)

    shipment.updated_at = datetime.utcnow()
    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    return shipment


@app.delete("/shipments/{shipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shipment(shipment_id: int, session: Session = Depends(get_session)) -> None:
    shipment = session.get(Shipment, shipment_id)
    if not shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")

    session.delete(shipment)
    session.commit()


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
