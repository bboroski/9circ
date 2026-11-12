CREATE TABLE IF NOT EXISTS ninecirc_documents (
    id UUID PRIMARY KEY,
    source TEXT NOT NULL,
    content TEXT NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_ninecirc_documents_updated_at
    ON ninecirc_documents (updated_at DESC);

CREATE TABLE IF NOT EXISTS ninecirc_artifacts (
    id UUID PRIMARY KEY,
    component TEXT NOT NULL,
    version TEXT NOT NULL,
    sha256 CHAR(64) NOT NULL,
    storage_uri TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (component, version),
    CHECK (sha256 ~ '^[0-9a-f]{64}$')
);

CREATE TABLE IF NOT EXISTS ninecirc_motivation_events (
    id BIGSERIAL PRIMARY KEY,
    node_id TEXT NOT NULL,
    reward DOUBLE PRECISION NOT NULL,
    cpu_pressure DOUBLE PRECISION NOT NULL,
    memory_pressure DOUBLE PRECISION NOT NULL,
    error_rate DOUBLE PRECISION NOT NULL,
    latency_ms DOUBLE PRECISION NOT NULL,
    observed_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_ninecirc_motivation_node_time
    ON ninecirc_motivation_events (node_id, observed_at DESC);
