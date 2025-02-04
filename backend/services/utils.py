from datetime import datetime, timedelta
from database.firebase import db

def delete_old_urls():
    """Deletes all shortened URLs older than a week."""
    
    delta = datetime.utcnow() - timedelta(days=7)

    urls_ref = db.collection("urls")

    old_urls = urls_ref.where("created_at", "<", delta).stream()
    
    for doc in old_urls:
        doc.reference.delete()

def get_salt(url: str) -> str:
    doc = db.collection("urls").document(url).get()
    if doc.exists:
        return doc.to_dict().get("salt")
    return None

def get_hash(url: str) -> str:
    doc = db.collection("urls").document(url).get()
    if doc.exists:
        return doc.to_dict().get("hash")
    return None