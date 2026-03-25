# Campus Bites Pipeline

Local PostgreSQL database for analyzing campus food delivery order data.

## Requirements

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Setup

**1. Clone the repo**

```bash
git clone <your-repo-url>
cd campus-bites-pipeline
```

**2. Start the database**

```bash
docker compose up -d
```

The database starts, creates the `orders` table, and loads the CSV automatically. This only runs once — data persists in a Docker volume between restarts.

**3. Connect and query**

Using `psql` (if installed locally):

```bash
psql -h localhost -U postgres -d campus_bites
```

Password: `postgres`

Or use a GUI client like [DBeaver](https://dbeaver.io/) or [TablePlus](https://tableplus.com/) with these connection details:

| Setting  | Value        |
|----------|--------------|
| Host     | localhost    |
| Port     | 5432         |
| Database | campus_bites |
| User     | postgres     |
| Password | postgres     |

## Example Queries

```sql
-- Preview the data
SELECT * FROM orders LIMIT 10;

-- Average order value by cuisine type
SELECT cuisine_type, ROUND(AVG(order_value), 2) AS avg_value
FROM orders
GROUP BY cuisine_type
ORDER BY avg_value DESC;

-- Orders by customer segment
SELECT customer_segment, COUNT(*) AS total_orders
FROM orders
GROUP BY customer_segment
ORDER BY total_orders DESC;
```

## Stopping the Database

```bash
docker compose down
```

To also delete all stored data:

```bash
docker compose down -v
```
