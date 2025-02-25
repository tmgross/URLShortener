from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.firebase import db
from firebase_admin import firestore
from services.url_shortener import generate_hash, generate_custom_alias

router = APIRouter()

class URLInput(BaseModel):
    url: str
    custom_alias: str = None
    salt: str = None
    hash: str = None
    uid: str = None

@router.post("/shorten")
async def shorten_url(data: URLInput):
    if data.custom_alias:
        if not generate_custom_alias(data.custom_alias, db):
            raise HTTPException(status_code=400, detail="Alias already in use.")
        shortened_url = data.custom_alias
    else:
        shortened_url = generate_hash(data.url)

    if not (data.url.startswith("http://") or data.url.startswith("https://")):
        data.url = "http://" + data.url
    
    # Check if the URL contains 'www.' if not, add it after the protocol
    if "://" in data.url:
        protocol_end = data.url.index("://") + 3
        domain_start = data.url[protocol_end:]
        if not domain_start.startswith("www."):
            data.url = data.url[:protocol_end] + "www." + domain_start

    if data.uid:
        db.collection("users").document(data.uid).update({
        "urls": firestore.ArrayUnion([shortened_url])
    })

    db.collection("urls").document(shortened_url).set({
        "original_url": data.url,
        "created_at": firestore.SERVER_TIMESTAMP,
        "salt": data.salt,
        "hash": data.hash
    })
    
    return {"shortened_url": shortened_url}