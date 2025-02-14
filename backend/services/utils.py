from datetime import datetime, timedelta
from database.firebase import db

def delete_old_urls():
    """Deletes all shortened URLs older than a week."""
    
    delta = datetime.utcnow() - timedelta(days=7)

    urls_ref = db.collection("urls")

    old_urls = urls_ref.where("created_at", "<", delta).stream()
    
    for doc in old_urls:
        doc.reference.delete()

"""
Utility functions for retrieving URL salts and hashes.
"""
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

"""
Utility functions for managing user account status in Firestore.
"""
def is_premium_account(uuid: str) -> bool:
    doc = db.collection("users").document(uuid).get()
    return doc.exists and doc.to_dict().get("premium", False)

def change_account_status(uuid: str):
    doc_ref = db.collection("users").document(uuid)
    doc = doc_ref.get()

    if not doc.exists:
        raise ValueError("User not found")

    current_status = doc.to_dict().get("premium", False)
    doc_ref.update({"premium": not current_status})
