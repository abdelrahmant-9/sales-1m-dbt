# Sales Analytics on 1M+ Rows — dbt + DuckDB

A beginner dbt project that transforms **1.2 million** sales transactions into
reporting tables: monthly revenue by category, revenue by region and channel,
and a customer summary with High / Medium / Low value levels.

Runs locally on **DuckDB**. `profiles.yml` also shows the settings for **Google BigQuery**.

## Flow

```
scripts/generate_data.py  ──►  raw.sales (1.2M) · raw.customers (50k) · raw.products (500) · raw.stores (40)
seeds/city_regions.csv    ──►  city_regions (city → country, region)
                                    │  dbt run
                                    ▼
                  staging (views)   stg_sales, stg_customers, stg_products, stg_stores
                                    ▼
                  marts (tables)    fct_sales
                                    monthly_category_sales
                                    region_channel_sales
                                    customer_summary
```

## What's inside
- **Sources** (`models/staging/_sources.yml`) for the raw tables
- **Seed** (`seeds/city_regions.csv`) — a small lookup table
- **Macro** (`macros/money.sql`) — rounds money to 2 decimals
- **Tests** — `unique`, `not_null`, `relationships`, `accepted_values` + one custom SQL test

## How to run
See [HOW_TO_RUN.md](HOW_TO_RUN.md).
