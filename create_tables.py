from app import models
from app.database import Base, engine

print("Membuat Tabel...")
Base.metadata.create_all(bind=engine)
print("Selesai")