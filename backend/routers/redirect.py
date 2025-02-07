from fastapi import APIRouter, HTTPException
from database.firebase import db
from firebase_admin import firestore

router = APIRouter()

@router.get("/{code}")
async def redirect_to_original(code: str):
    """Redirect to the original URL based on the shortened code."""
    doc = db.collection("urls").document(code).get()
    
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Shortened URL not found")
    
    original_url = doc.to_dict().get("original_url")

    clicks_doc_ref = db.collection("urls").document(code).collection("analytics").document("clicks")

    clicks_doc_ref.set({
        "num": firestore.Increment(1)
    }, merge=True)

    return {"url": original_url}