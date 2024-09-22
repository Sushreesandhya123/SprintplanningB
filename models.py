from sqlalchemy import Column, Integer, String, Enum
from database import Base
import enum

class StatusEnum(enum.Enum):
    DONE = "Done"
    BACKLOG = "Backlog"
    PENDING = "Pending"

class Sprintgoal(Base):
    __tablename__ = 'sprintgoal'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(300))
    status = Column(Enum(StatusEnum), nullable=False)


