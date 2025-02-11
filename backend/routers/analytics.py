from fastapi import APIRouter, HTTPException
from database.firebase import db
from collections import defaultdict

router = APIRouter()

@router.get("/{code}/referrers")
async def get_refferer_counts(code: str):
    """Get a dictionary of all referrers and their counts."""
    visits_ref = db.collection("urls").document(code).collection("visits")
    visits = visits_ref.stream()

    referrer_counts = defaultdict(int)

    for visit in visits:
        referrer = visit.to_dict().get("referrer", "Direct")
        referrer_counts[referrer] += 1

    return {"referrers": dict(referrer_counts)}

@router.get("/{code}/access-dates")
async def get_access_dates(code: str):
    """Get a dictionary of all access dates and their counts."""
    visits_ref = db.collection("urls").document(code).collection("visits")
    visits = visits_ref.stream()

    date_counts = defaultdict(int)

    for visit in visits:
        timestamp = visit.to_dict().get("timestamp")
        if timestamp:
            date = timestamp.strftime("%Y-%m-%d")  # Format as YYYY-MM-DD
            date_counts[date] += 1

    return {"access_dates": dict(date_counts)}