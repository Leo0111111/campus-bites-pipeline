# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Campus Bites Pipeline is a local ETL tool that loads 1,132 campus food delivery orders from a CSV into a Dockerized PostgreSQL database for analysis.

## Running the Pipeline

```bash
# Start the database (first time or after `down -v`)
docker compose up -d

# Load CSV data into the database (idempotent — safe to run multiple times)
python load_data.py

# Connect via psql
psql -h localhost -U postgres -d campus_bites   # password: postgres

# Stop the database (data persists in Docker volume)
docker compose down

# Stop and wipe all data
docker compose down -v
```

## Architecture

The pipeline has two components:

- **Docker Compose** (`docker-compose.yml`): Runs PostgreSQL 16 on port 5432, database `campus_bites`, user/password `postgres`.
- **Data loader** (`load_data.py`): Connects via `psycopg2`, creates the `orders` table with `IF NOT EXISTS`, reads `data/campus_bites_orders.csv` with `csv.DictReader`, converts `"Yes"`/`"No"` strings to booleans via `parse_bool()`, then bulk-inserts with `executemany()`. Uses `ON CONFLICT (order_id) DO NOTHING` for idempotency.

## Database Schema

Single table `orders`:

| Column | Type |
|---|---|
| `order_id` | `INTEGER PRIMARY KEY` |
| `order_date` | `DATE` |
| `order_time` | `TIME` |
| `customer_segment` | `TEXT` (Dorm, Off-Campus, Grad Student, Greek Life) |
| `order_value` | `NUMERIC(10,2)` |
| `cuisine_type` | `TEXT` (Asian, Indian, Breakfast, Pizza, Greek, Mediterranean, Burgers, Mexican) |
| `delivery_time_mins` | `INTEGER` |
| `promo_code_used` | `BOOLEAN` |
| `is_reorder` | `BOOLEAN` |

## Dependencies

- `psycopg2-binary==2.9.11` (see `requirements.txt`)
- Docker Desktop must be running before `docker compose up -d`
