from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, HttpUrl
from typing import Union
from services.utils import get_hash, get_salt
from database.firebase import db

router = APIRouter()

@router.get("/{code}/salt")
async def fetch_salt(code: str):
    """Fetch the salt for the shortened URL."""
    salt = get_salt(code)
    if not salt:
        return {"salt": None}
    return {"salt": salt}

@router.get("/{code}/hash")
async def fetch_hash(code: str):
    """Fetch the password hash for the shortened URL."""
    password_hash = get_hash(code)
    if not password_hash:
        return {"password_hash": None}
    return {"password_hash": password_hash}


# TODO: figure out where to store images, and update this path
pdf_path = "temp"

@router.get("/{code}/get")
async def get_pdf(code: str):
    """Retrieve the base PDF associated with the shortened URL."""
    doc = db.collection("urls").document(code).get
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Shortened URL not found")
    
    # TODO: update ref with where image is stored
    pdf_ref = pdf_path + code + ".pdf"

    if not pdf_ref:
        raise HTTPException(status_code=404, detail="PDF not found") 

    return FileResponse(pdf_ref, media_type="application/pdf", filename=f"{code}.pdf")


@router.get("/{code}/set")
async def set_pdf(code: str):
    """Upload a PDF to be associated with the shortened URL."""
    doc = db.collection("urls").document(code).get

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Shortened URL not found")

    # TODO: update ref with where image is stored
    pdf_ref = pdf_path + code + ".pdf"

    if not pdf_ref:
        raise HTTPException(status_code=404, detail="PDF not found") 

    # TODO: store the file in whichever service we decide on,
    #  and store location of file in firebase

    return {"message": "PDF uploaded successfully", "pdf_url": f"/{code}/get"}

class AnnotationBase(BaseModel):
    id: int
    x: int
    y: int
    width: int
    height: int
    scale: int
    type: str
    required: bool = False

# Text annotation
class TextAnnotation(AnnotationBase):
    type: str = "text"
    text: str

# Signature annotation
class SignatureAnnotation(AnnotationBase):
    type: str = "signature"
    file: str = None
    url: HttpUrl
    naturalWidth: int
    naturalHeight: int

# Image annotation
class ImageAnnotation(AnnotationBase):
    type: str = "image"
    file: str = None
    url: HttpUrl
    naturalWidth: int
    naturalHeight: int

# Checkbox annotation
class CheckboxAnnotation(AnnotationBase):
    type: str = "checkbox"
    checked: bool = False

# Union type to allow multiple annotation types
AnnotationTypes = Union[TextAnnotation, SignatureAnnotation, ImageAnnotation, CheckboxAnnotation]


@router.get("/{code}/annotate")
async def annotate(code: str, annotation: AnnotationTypes):
    if annotation.type in ["signature", "image"]:
        # TODO:
        # - store image in some service
        # - get url of where its stored and update the url field in annotation
        # - store the information in firebase
        return
    else:
        # TODO: should the id be stored with the rest of the information
        # it is currently the name of the document
        # for annotation retrieval it would be easier to also store it with the other information
        annotation_data = annotation.model_dump()
        annotation_id = str(annotation_data.pop(("id")))

        doc_ref = db.collection("urls").document(code).collection("annotations").document(annotation_id)
        
        if doc_ref.get().exists:
            return HTTPException(status_code=400, detail="Annotation already exists")
        
        doc_ref.set(annotation.data)

    return {"message": "Annotation saved", "annotation": annotation}