from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas
from app.auth_dep import get_current_user

router = APIRouter(prefix="/categories", tags=["Categories"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.Category])
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()


@router.post("/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(get_current_user)):
    existing = db.query(models.Category).filter(models.Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    new_category = models.Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.put("/{category_id}", response_model=schemas.Category)
def update_category(category_id: int, updated_category: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(get_current_user)):
    category = db.query(models.Category).get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    for key, value in updated_category.dict().items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)
    return category


@router.get("/{category_id}", response_model=schemas.Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(get_current_user)):
    category = db.query(models.Category).get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"message": "Category deleted"}