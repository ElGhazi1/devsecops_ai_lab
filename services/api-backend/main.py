from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
import httpx
import os

from models import Product
from database import get_db, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Backend", version="1.0.0")

OAUTH2_URL = os.getenv("OAUTH2_URL", "http://localhost:8001")


async def verify_oauth_token(authorization: Optional[str] = Header(None)) -> dict:
    """Verify token with OAuth2 service"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")

    token = authorization.replace("Bearer ", "")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{OAUTH2_URL}/me", headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid token")
        return response.json()


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "api-backend"}


@app.post("/products")
async def create_product(
    name: str,
    description: str,
    price: float,
    user: dict = Depends(verify_oauth_token),
    db: Session = Depends(get_db),
):
    product = Product(name=name, description=description, price=price, owner_id=user["id"])
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@app.get("/products")
async def list_products(
    user: dict = Depends(verify_oauth_token), db: Session = Depends(get_db)
):
    products = db.query(Product).filter(Product.owner_id == user["id"]).all()
    return products


@app.get("/products/{product_id}")
async def get_product(
    product_id: int,
    user: dict = Depends(verify_oauth_token),
    db: Session = Depends(get_db),
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id, Product.owner_id == user["id"])
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
