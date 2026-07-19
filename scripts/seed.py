"""Dev seed: illustrative brand + a couple of documents so the API returns something locally.

Run after `alembic upgrade head`. Intentionally tiny — real estates arrive via ingestion.
"""
from __future__ import annotations

DEMO_BRAND = {"brand_id": "brand_demo", "name": "Demo Brand"}

# See tests/ for how the in-memory adapters are used without a database.
if __name__ == "__main__":
    print("Seed is a placeholder; wire to the repositories once implementations land.")
