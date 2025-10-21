from database import Base
from sqlalchemy import ForeignKey,create_engine,DateTime,func,String,Integer,Column
from sqlalchemy.orm import relationship
from database import engine



class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True)
    task_desc = Column(String, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    container = Column(Integer, ForeignKey('collections.id'), nullable=True)

    collections = relationship("Collection", back_populates="tasks")


    
        

class Collection(Base):
    __tablename__ = 'collections'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    tasks = relationship("Task", back_populates="collections")


Base.metadata.create_all(engine)