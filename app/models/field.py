from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.dialects.postgresql import ARRAY
from app.db.database import Base

class Field(Base):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    coordinates = Column(ARRAY(Float), nullable=False)         
    surface_type = Column(String, nullable=True)               
    format = Column(String, nullable=True)                     
    hidden = Column(Boolean, nullable=False, default=False)
    featured = Column(Boolean, nullable=False, default=False)
    lighting = Column(Boolean, default=False)
    parking = Column(Boolean, default=False)
    accessibility = Column(Boolean, default=False)             
    phone = Column(String, nullable=True)
    website = Column(String, nullable=True)
    borough = Column(String, nullable=True)
    description = Column(String, nullable=True)
    amenities = Column(ARRAY(String), nullable=True)           
    rating = Column(Float, nullable=True)
    reviews = Column(Integer, nullable=True)
    photos = Column(ARRAY(String), nullable=True)
