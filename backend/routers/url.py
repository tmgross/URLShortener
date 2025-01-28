from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.firebase import db
from firebase_admin import firestore
from services.url_shortener import generate_hash, generate_custom_alias

router = APIRouter()

class URLInput(BaseModel):
    url: str
    custom_alias: str = None

@router.post("/shorten")
async def shorten_url(data: URLInput):
    if data.custom_alias:
        if not generate_custom_alias(data.custom_alias, db):
            raise HTTPException(status_code=400, detail="Alias already in use.")
        shortened_url = data.custom_alias
    else:
        shortened_url = generate_hash(data.url)

    db.collection("urls").document(shortened_url).set({
        "original_url": data.url,
        "created_at": firestore.SERVER_TIMESTAMP
    })
    
    return {"shortened_url": shortened_url}