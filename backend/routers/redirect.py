from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
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
    
    db.collection("urls").document(code).collection("analytics").add({
        "timestamp": firestore.SERVER_TIMESTAMP,
    })
    
    # Redirect to the original URL
    return RedirectResponse(url=original_url)