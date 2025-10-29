
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List
import datetime

from ..deps import FirestoreClient, CurrentUser

router = APIRouter()

class Product(BaseModel):
    name: str
    description: str
    price: float
    owner_id: str | None = None

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(product: Product, db: FirestoreClient, user: CurrentUser):
    """Create a new product, associating it with the current user."""
    product.owner_id = user["uid"]
    try:
        doc_ref = db.collection("products").document()
        await doc_ref.set(product.model_dump())
        return {"id": doc_ref.id, **product.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/", response_model=List[Product])
async def get_products(db: FirestoreClient):
    """Get a list of all products."""
    products = []
    try:
        docs = db.collection("products").stream()
        async for doc in docs:
            products.append(Product(**doc.to_dict()))
        return products
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
