from sqlalchemy import Column, Integer, Time, String
from database import Base


class RobotRecords(Base):
    __tablename__ = "Launches"
    id = Column(Integer, primary_key=True, index=True)
    time_launch = Column(Time)
    duration = Column(String)
    start_value = Column(Integer)
