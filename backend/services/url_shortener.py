import hashlib
import random
import string

def generate_hash(url: str, length: int = 6) -> str:
    """Generates a unique hash for the given URL"""
    hash_object = hashlib.sha256(url.encode())
    hash_hex = hash_object.hexdigest()
    return hash_hex[:length]

def generate_custom_alias(custom_alias: str, db) -> bool:
    """Check if the custom alias is unique in the database"""
    doc = db.collection("urls").document(custom_alias).get()
    return not doc.exists