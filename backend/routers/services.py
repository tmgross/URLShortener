from fastapi import APIRouter, HTTPException
from services.utils import get_hash, get_salt

router = APIRouter()

@router.get("/{code}/salt")
async def fetch_salt(code: str):
    """Fetch the salt for the shortened URL."""
    salt = get_salt(code)
    if not salt:
        raise HTTPException(status_code=404, detail="Salt not found")
    return {"salt": salt}

@router.get("/{code}/hash")
async def fetch_hash(code: str):
    """Fetch the password hash for the shortened URL."""
    password_hash = get_hash(code)
    if not password_hash:
        raise HTTPException(status_code=404, detail="Hash not found")
    return {"password_hash": password_hash}
