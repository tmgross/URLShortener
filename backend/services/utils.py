from datetime import datetime, timedelta
from database.firebase import db

def delete_old_urls():
    """Deletes all shortened URLs older than a week."""
    
    delta = datetime.utcnow() - timedelta(days=7)

    urls_ref = db.collection("urls")

    old_urls = urls_ref.where("created_at", "<", delta).stream()
    
    for doc in old_urls:
        doc.reference.delete()