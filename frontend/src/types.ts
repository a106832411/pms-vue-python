export type ShipmentStatus =
  | "created"
  | "in_transit"
  | "delivered"
  | "canceled";

export type Shipment = {
  id: number;
  tracking_number: string;
  shipper: string;
  consignee: string;
  origin: string;
  destination: string;
  carrier?: string | null;
  status: ShipmentStatus;
  pieces: number;
  weight_kg: number;
  cost: number;
  pickup_date?: string | null;
  expected_delivery?: string | null;
  delivered_at?: string | null;
  notes?: string | null;
  created_at: string;
  updated_at: string;
};

export type ShipmentPayload = {
  tracking_number: string;
  shipper: string;
  consignee: string;
  origin: string;
  destination: string;
  carrier?: string | null;
  status: ShipmentStatus;
  pieces: number;
  weight_kg: number;
  cost: number;
  pickup_date?: string | null;
  expected_delivery?: string | null;
  delivered_at?: string | null;
  notes?: string | null;
};

export type ShipmentList = {
  total: number;
  items: Shipment[];
};
