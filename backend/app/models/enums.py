import enum

class PurchaseSource(str, enum.Enum):
    original_store = "original_store"
    third_party = "third_party"

class ProductCondition(str, enum.Enum):
    like_new = "like_new"
    used = "used"
    damaged = "damaged"

class RMAStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    awaiting_return = "awaiting_return"
    received = "received"
    closed = "closed"


class RMADecision(str, enum.Enum):
    refund_eligible = "refund_eligible"
    replacement_eligible = "replacement_eligible"
    rejected = "rejected"

class ShipmentDirection(str, enum.Enum):
    inbound = "inbound"
    outbound = "outbound"


class ShipmentStatus(str, enum.Enum):
    label_created = "label_created"
    in_transit = "in_transit"
    delivered = "delivered"
    exception = "exception"
    cancelled = "cancelled"

class RefundStatus(str, enum.Enum):
    queued = "queued"
    processed = "processed"
    failed = "failed"
    voided = "voided"

class InspectionSource(str, enum.Enum):
    customer = "customer"
    agent = "agent"
    warehouse = "warehouse"
    automated_test = "automated_test"

class EventType(str, enum.Enum):
    REQUEST_CREATED = "REQUEST_CREATED"
    POLICY_EVALUATED = "POLICY_EVALUATED"
    DECISION_MADE = "DECISION_MADE"
    RMA_NUMBER_ISSUED = "RMA_NUMBER_ISSUED"
    LABEL_CREATED = "LABEL_CREATED"
    ITEM_RECEIVED = "ITEM_RECEIVED"
    INSPECTION_RECORDED = "INSPECTION_RECORDED"
    REFUND_QUEUED = "REFUND_QUEUED"
    REFUND_PROCESSED = "REFUND_PROCESSED"
    REPLACEMENT_SHIPPED = "REPLACEMENT_SHIPPED"
    CASE_CLOSED = "CASE_CLOSED"