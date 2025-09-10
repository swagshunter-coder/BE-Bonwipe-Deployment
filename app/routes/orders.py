from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from typing import List, Optional
from app.auth_dep import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=schemas.OrderOut)
def create_order(order_data: schemas.OrderCreate, db: Session = Depends(get_db)):
    order = models.Order(
        customer_name=order_data.customer_name,
        customer_email=order_data.customer_email,
        customer_phone=order_data.customer_phone,
        shipping_address=order_data.shipping_address,
        bank_id=order_data.bank_id,
        transfer_proof=order_data.transfer_proof,
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    for item_data in order_data.items:
        product = db.query(models.Product).filter(models.Product.id == item_data.product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail=f"Product ID {item_data.product_id} not found")

        if product.stock < item_data.quantity:
            raise HTTPException(status_code=400, detail=f"Stock not enough for product '{product.name}'")

        # ✅ Kurangi stok
        product.stock -= item_data.quantity

        order_item = models.OrderItem(
            order_id=order.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity,
            price_at_order=product.price
        )
        db.add(order_item)

    db.commit()
    db.refresh(order)
    return order

@router.get("/", response_model=List[schemas.OrderOut])
def get_all_orders(db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(get_current_user)):
    orders = db.query(models.Order).all()
    return orders


@router.put("/status/{order_id}", response_model=schemas.OrderOut)
def update_order_status(order_id: int, status_update: schemas.OrderStatusUpdate, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(get_current_user)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status_update.status
    db.commit()
    db.refresh(order)

    return order


@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(get_current_user)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}

@router.get("/active", response_model=List[schemas.OrderOut])
def get_active_orders(
    email : str,
    phone : str,
    db: Session = Depends(get_db)
):
    active_statuses = ["pending", "diproses", "dikirim"]
    orders = db.query(models.Order).filter(
        models.Order.customer_email == email,
        models.Order.customer_phone == phone,
        models.Order.status.in_(active_statuses)
    ).all()

    if not orders:
        raise HTTPException(status_code=404, detail="Tidak ada pesanan aktif ditemukan.")
    
    return orders

@router.get("/history", response_model=List[schemas.OrderOut])
def get_order_history(
    email: str,
    phone: str,
    db: Session = Depends(get_db)
):
    orders = db.query(models.Order).filter(
        models.Order.customer_email == email,
        models.Order.customer_phone == phone
    ).order_by(models.Order.created_at.desc()).all()

    if not orders:
        raise HTTPException(status_code=404, detail="Riwayat pesanan tidak ditemukan.")
    
    return orders

@router.get("/{order_id}", response_model=schemas.OrderDetailOut)
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    total = sum(item.quantity * item.price_at_order for item in order.items)

    return {
        **order.__dict__,
        "items": order.items,
        "total": total
    }

