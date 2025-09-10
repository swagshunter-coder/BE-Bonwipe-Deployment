from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models
from app.database import get_db
from app.auth_dep import get_current_user
from app.schemas import UserOut

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/summary")
def get_admin_summary(
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    name = current_user.full_name if current_user.full_name else "Admin"
    total_products = db.query(models.Product).count()
    total_orders = db.query(models.Order).count()
    pending_orders = db.query(models.Order).filter(models.Order.status == "pending").count()
    completed_orders = db.query(models.Order).filter(models.Order.status == "selesai").count()

    # Total pendapatan (dari semua order item)
    total_income = db.query(models.OrderItem).join(models.Order).filter(
        models.Order.status == "selesai"
    ).with_entities(
        models.OrderItem.price_at_order * models.OrderItem.quantity
    ).all()

    total_income_sum = sum([amount[0] for amount in total_income]) if total_income else 0

    return {
        "name": name,
        "total_products": total_products,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "total_income": total_income_sum
    }
