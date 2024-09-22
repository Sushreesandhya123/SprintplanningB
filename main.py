from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
import models
from database import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware

# Create the FastAPI app
app = FastAPI()

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Allow CORS for your frontend URL (adjust as needed)
origins = [
    "http://localhost:3000",  # React app URL
    # Add other origins if necessary
]

# Add CORS middleware to allow the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for Sprintgoal
class SprintgoalBase(BaseModel):
    description: str
    status: str

class SprintgoalCreate(SprintgoalBase):
    pass

class SprintgoalUpdate(SprintgoalBase):
    pass

class Sprintgoal(SprintgoalBase):
    id: int

    class Config:
        orm_mode = True

# Dependency to get the database session
def get_db():
    db = SessionLocal()  
    try:
        yield db  
    finally:
        db.close()  

# Create a new sprint goal
@app.post("/sprintgoals/", response_model=Sprintgoal)
def create_sprintgoal(sprintgoal: SprintgoalCreate, db: Session = Depends(get_db)):
    db_sprintgoal = models.Sprintgoal(**sprintgoal.dict())
    db.add(db_sprintgoal)
    db.commit()
    db.refresh(db_sprintgoal)
    return db_sprintgoal

# Read all sprint goals
@app.get("/sprintgoals/", response_model=List[Sprintgoal])
def read_sprintgoals(db: Session = Depends(get_db)):
    sprintgoals = db.query(models.Sprintgoal).all()
    return sprintgoals

# Read a specific sprint goal by ID
@app.get("/sprintgoals/{sprintgoal_id}", response_model=Sprintgoal)
def read_sprintgoal(sprintgoal_id: int, db: Session = Depends(get_db)):
    sprintgoal = db.query(models.Sprintgoal).filter(models.Sprintgoal.id == sprintgoal_id).first()
    if sprintgoal is None:
        raise HTTPException(status_code=404, detail="Sprintgoal not found")
    return sprintgoal

# Update an existing sprint goal
@app.put("/sprintgoals/{sprintgoal_id}", response_model=Sprintgoal)
def update_sprintgoal(sprintgoal_id: int, sprintgoal: SprintgoalUpdate, db: Session = Depends(get_db)):
    db_sprintgoal = db.query(models.Sprintgoal).filter(models.Sprintgoal.id == sprintgoal_id).first()
    if db_sprintgoal is None:
        raise HTTPException(status_code=404, detail="Sprintgoal not found")
    for key, value in sprintgoal.dict().items():
        setattr(db_sprintgoal, key, value)
    db.commit()
    db.refresh(db_sprintgoal)
    return db_sprintgoal

# Delete a sprint goal
@app.delete("/sprintgoals/{sprintgoal_id}")
def delete_sprintgoal(sprintgoal_id: int, db: Session = Depends(get_db)):
    db_sprintgoal = db.query(models.Sprintgoal).filter(models.Sprintgoal.id == sprintgoal_id).first()
    if db_sprintgoal is None:
        raise HTTPException(status_code=404, detail="Sprintgoal not found")
    db.delete(db_sprintgoal)
    db.commit()
    return {"detail": "Sprintgoal deleted"}
