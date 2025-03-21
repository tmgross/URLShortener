from fastapi import APIRouter, HTTPException
from database.firebase import db
from collections import defaultdict

router = APIRouter()
@router.get("/{uid}/urls")
async def get_user_urls(uid: str):
    user_ref = db.collection("users").document(uid)
    user_doc = user_ref.get()

    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="User not found")
    
    urls_ref = user_ref.collection("urls")
    docs = urls_ref.stream()

    urls_dict = {}
    for doc in docs:
        doc_data = doc.to_dict()
        urls_dict[doc.id] = doc_data.get("urls", [])

    return {"groups": urls_dict}

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