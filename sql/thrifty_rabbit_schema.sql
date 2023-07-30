CREATE TABLE assets (
    symbol TEXT PRIMARY KEY NOT NULL,
    asset_name TEXT,
    sector TEXT
);

CREATE TABLE portfolios (
    id INTEGER PRIMARY KEY NOT NULL,
    asset_name TEXT,
    risk_bucket INTEGER 
);

CREATE TABLE portfolio_assets (
  id INTEGER PRIMARY KEY NOT NULL,
  portfolio_id INTEGER REFERENCES portfolios (id) NOT NULL,
  asset_symbol TEXT REFERENCES assets (symbol) NOT NULL
);

CREATE TABLE risk_buckets (
  id INTEGER PRIMARY KEY,
  capacity_min INTEGER,
  capacity_max INTEGER,
  tolerance_max INTEGER,
  tolerance_min INTEGER,
  portfolio_id INTEGER REFERENCES portfolios (id)
);
