from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from typing import List, Optional
from app.auth_dep import get_current_user

router = APIRouter(prefix="/banks", tags=["Banks"])

@router.post("/", response_model=schemas.BankOut)
def create_bank(bank: schemas.BankCreate, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(get_current_user)):
    new_bank = models.Bank(**bank.dict())
    db.add(new_bank)
    db.commit()
    db.refresh(new_bank)
    return new_bank

@router.get("/", response_model=List[schemas.BankOut])
def get_banks(db: Session = Depends(get_db)):
    return db.query(models.Bank).all()

@router.put("/{bank_id}", response_model=schemas.BankOut)
def update_bank(bank_id: int, bank_update: schemas.BankCreate, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(get_current_user)):
    bank = db.query(models.Bank).filter(models.Bank.id == bank_id).first()
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")

    bank.name = bank_update.name
    bank.account_number = bank_update.account_number
    db.commit()
    db.refresh(bank)
    return bank

@router.delete("/{bank_id}")
def delete_bank(bank_id: int, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(get_current_user)):
    bank = db.query(models.Bank).filter(models.Bank.id == bank_id).first()
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")
    
    db.delete(bank)
    db.commit()
    return {"message": "Bank deleted successfully"}