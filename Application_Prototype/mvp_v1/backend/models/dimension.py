from sqlalchemy import Column, Integer, String, Float
from database import Base

class Dimension(Base):
    __tablename__ = "dimensions"

    dimension_id = Column(Integer, primary_key=True, index=True)
    dimension_name = Column(String)
    dimension_name_de = Column(String)
    dimension_weight = Column(Float)
