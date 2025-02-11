from fastapi import APIRouter, HTTPException, Request
from database.firebase import db
from firebase_admin import firestore

router = APIRouter()

@router.get("/{code}")
async def redirect_to_original(code: str, request: Request):
    """Redirect to the original URL based on the shortened code."""
    doc_ref = db.collection("urls").document(code)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Shortened URL not found")
    
    # Store visit details
    visit_data = {
        "timestamp": firestore.SERVER_TIMESTAMP,
        "ip": request.client.host,
        "user_agent": request.headers.get("User-Agent"),
        "referrer": request.headers.get("Referer")
    }

    visit_ref = doc_ref.collection("visits").document()
    visit_ref.set(visit_data)

    # Update aggregate details
    analytics_ref = doc_ref.collection("analytics").document("clicks")
    analytics_ref.set({
        "num": firestore.Increment(1),
        "last_accessed": firestore.SERVER_TIMESTAMP
    }, merge=True)

    original_url = doc.to_dict().get("original_url")

    return {"url": original_url}