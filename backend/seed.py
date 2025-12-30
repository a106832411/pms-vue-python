import argparse
import random
from datetime import date, datetime, timedelta

from sqlmodel import Session

from app.database import engine, init_db
from app.models import Shipment, ShipmentStatus

CARRIERS = ["顺丰", "京东", "德邦", "邮政", "中通", "极兔"]
CITIES = ["北京", "上海", "广州", "深圳", "杭州", "成都", "武汉", "西安", "南京", "重庆"]
SHIPPERS = ["华东仓", "华南仓", "华北仓", "华中仓"]
CONSIGNEES = ["客户A", "客户B", "客户C", "客户D", "客户E"]


def build_shipment(idx: int) -> Shipment:
    pickup = date.today() - timedelta(days=random.randint(0, 10))
    expected = pickup + timedelta(days=random.randint(1, 6))

    status = random.choices(
        [ShipmentStatus.CREATED, ShipmentStatus.IN_TRANSIT, ShipmentStatus.DELIVERED, ShipmentStatus.CANCELED],
        weights=[2, 4, 3, 1],
        k=1,
    )[0]

    delivered_at = None
    if status == ShipmentStatus.DELIVERED:
        delivered_at = datetime.combine(expected, datetime.min.time()) + timedelta(hours=random.randint(9, 18))

    weight_kg = round(random.uniform(1.0, 80.0), 2)
    cost = round(weight_kg * random.uniform(3.5, 6.5), 2)

    return Shipment(
        tracking_number=f"TMS-{1000 + idx:05d}",
        shipper=random.choice(SHIPPERS),
        consignee=random.choice(CONSIGNEES),
        origin=random.choice(CITIES),
        destination=random.choice(CITIES),
        carrier=random.choice(CARRIERS),
        status=status,
        pieces=random.randint(1, 6),
        weight_kg=weight_kg,
        cost=cost,
        pickup_date=pickup,
        expected_delivery=expected,
        delivered_at=delivered_at,
        notes=None,
    )


def seed(count: int) -> None:
    init_db()
    with Session(engine) as session:
        items = [build_shipment(i) for i in range(count)]
        session.add_all(items)
        session.commit()
    print(f"Inserted {count} shipments.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed shipments")
    parser.add_argument("--count", type=int, default=100, help="Number of shipments to create")
    args = parser.parse_args()
    seed(args.count)


if __name__ == "__main__":
    main()
