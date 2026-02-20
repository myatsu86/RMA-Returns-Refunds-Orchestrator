DO $$ BEGIN
  CREATE TYPE purchase_source_enum AS ENUM ('original_store', 'third_party');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE product_condition_enum AS ENUM ('like_new', 'used', 'damaged');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE rma_status_enum AS ENUM ('pending', 'approved', 'rejected', 'awaiting_return', 'received', 'closed');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE rma_decision_enum AS ENUM ('refund_eligible', 'replacement_eligible', 'rejected');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE shipment_direction_enum AS ENUM ('inbound', 'outbound');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE shipment_status_enum AS ENUM ('label_created', 'in_transit', 'delivered', 'exception', 'cancelled');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE refund_status_enum AS ENUM ('queued', 'processed', 'failed', 'voided');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE inspection_source_enum AS ENUM ('customer', 'agent', 'warehouse', 'automated_test');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE event_type_enum AS ENUM ('REQUEST_CREATED', 'POLICY_EVALUATED', 'DECISION_MADE', 'RMA_NUMBER_ISSUED', 'LABEL_CREATED', 'ITEM_RECEIVED', 'INSPECTION_RECORDED', 'REFUND_QUEUED', 'REFUND_PROCESSED', 'REPLACEMENT_SHIPPED', 'CASE_CLOSED');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

CREATE TABLE IF NOT EXISTS products (
  serial_number TEXT PRIMARY KEY,
  warranty_expires_at DATE NOT NULL,
  model TEXT,
  sku TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_products_warranty_expires_at ON products (warranty_expires_at);
CREATE INDEX IF NOT EXISTS idx_products_sku ON products (sku);

CREATE TABLE IF NOT EXISTS rma_requests (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  serial_number TEXT NOT NULL REFERENCES products(serial_number),
  purchase_source purchase_source_enum NOT NULL,
  delivery_date DATE,
  customer_reported_condition product_condition_enum,
  data_responsibility_acknowledged BOOLEAN NOT NULL DEFAULT FALSE,
  status rma_status_enum NOT NULL DEFAULT 'pending',
  decision rma_decision_enum,
  decision_reason TEXT,
  decided_at TIMESTAMPTZ,
  rma_number TEXT UNIQUE,
  warranty_checked_at TIMESTAMPTZ,
  warranty_valid BOOLEAN,
  CONSTRAINT chk_decision_timestamp_consistency CHECK ((decision IS NULL AND decided_at IS NULL) OR (decision IS NOT NULL AND decided_at IS NOT NULL)),
  CONSTRAINT chk_status_decision_consistency CHECK ((status = 'rejected' AND decision = 'rejected') OR (status <> 'rejected'))
);

CREATE INDEX IF NOT EXISTS idx_rma_requests_serial_created ON rma_requests (serial_number, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_rma_requests_status ON rma_requests (status);
CREATE INDEX IF NOT EXISTS idx_rma_requests_decision ON rma_requests (decision);
CREATE INDEX IF NOT EXISTS idx_rma_requests_created_at ON rma_requests (created_at DESC);
CREATE UNIQUE INDEX IF NOT EXISTS idx_rma_requests_rma_number ON rma_requests (rma_number) WHERE rma_number IS NOT NULL;

CREATE TABLE IF NOT EXISTS rma_inspections (
  id BIGSERIAL PRIMARY KEY,
  rma_request_id BIGINT NOT NULL REFERENCES rma_requests(id) ON DELETE CASCADE,
  inspected_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  source inspection_source_enum NOT NULL DEFAULT 'warehouse',
  inspector_id TEXT,
  hardware_failure_confirmed BOOLEAN NOT NULL DEFAULT FALSE,
  failure_notes TEXT,
  verified_condition product_condition_enum,
  condition_notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_rma_inspections_request_time ON rma_inspections (rma_request_id, inspected_at DESC);

CREATE TABLE IF NOT EXISTS return_shipments (
  id BIGSERIAL PRIMARY KEY,
  rma_request_id BIGINT NOT NULL REFERENCES rma_requests(id) ON DELETE CASCADE,
  direction shipment_direction_enum NOT NULL,
  carrier TEXT,
  tracking_number TEXT,
  label_provided_by_seagate BOOLEAN NOT NULL DEFAULT FALSE,
  shipping_cost_payer TEXT NOT NULL CHECK (shipping_cost_payer IN ('customer', 'seagate')),
  status shipment_status_enum NOT NULL DEFAULT 'label_created',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  delivered_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_return_shipments_request ON return_shipments (rma_request_id);
CREATE INDEX IF NOT EXISTS idx_return_shipments_tracking ON return_shipments (tracking_number);

CREATE TABLE IF NOT EXISTS refund_transactions (
  id BIGSERIAL PRIMARY KEY,
  rma_request_id BIGINT NOT NULL REFERENCES rma_requests(id) ON DELETE CASCADE,
  amount_cents BIGINT NOT NULL CHECK (amount_cents > 0),
  currency TEXT NOT NULL DEFAULT 'USD' CHECK (currency IN ('USD', 'EUR', 'GBP')),
  status refund_status_enum NOT NULL DEFAULT 'queued',
  payment_method TEXT,
  processor_reference TEXT,
  queued_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  processed_at TIMESTAMPTZ,
  failure_reason TEXT,
  CONSTRAINT chk_refund_processed_at_consistency CHECK ((status = 'processed' AND processed_at IS NOT NULL) OR (status <> 'processed'))
);

CREATE INDEX IF NOT EXISTS idx_refunds_request ON refund_transactions (rma_request_id);
CREATE INDEX IF NOT EXISTS idx_refunds_status ON refund_transactions (status);

CREATE TABLE IF NOT EXISTS rma_policy_log (
  id BIGSERIAL PRIMARY KEY,
  rma_request_id BIGINT NOT NULL REFERENCES rma_requests(id) ON DELETE CASCADE,
  policy_id TEXT NOT NULL CHECK (policy_id ~ '^P[0-9]+$'),
  policy_version TEXT NOT NULL DEFAULT 'v1',
  engine_version TEXT NOT NULL DEFAULT 'rules-v1',
  evaluated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  matched BOOLEAN NOT NULL,
  outcome TEXT NOT NULL,
  details JSONB
);

CREATE INDEX IF NOT EXISTS idx_policylog_request_time ON rma_policy_log (rma_request_id, evaluated_at DESC);
CREATE INDEX IF NOT EXISTS idx_policylog_policy_id ON rma_policy_log (policy_id);

CREATE TABLE IF NOT EXISTS rma_events (
  id BIGSERIAL PRIMARY KEY,
  rma_request_id BIGINT NOT NULL REFERENCES rma_requests(id) ON DELETE CASCADE,
  event_type event_type_enum NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  actor_type TEXT,
  actor_id TEXT,
  message TEXT,
  meta JSONB
);

CREATE INDEX IF NOT EXISTS idx_rma_events_request_time ON rma_events (rma_request_id, created_at DESC);

CREATE OR REPLACE VIEW v_rma_latest_inspection AS
SELECT DISTINCT ON (ri.rma_request_id)
  ri.rma_request_id, ri.inspected_at, ri.source, ri.inspector_id,
  ri.hardware_failure_confirmed, ri.verified_condition, ri.failure_notes, ri.condition_notes
FROM rma_inspections ri
ORDER BY ri.rma_request_id, ri.inspected_at DESC;
