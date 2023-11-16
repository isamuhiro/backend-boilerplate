from sqlalchemy import UUID, Boolean, Column, DateTime, Numeric, String
from sqlalchemy.orm import declarative_base

from domain.entities.account import Account

Base = declarative_base()


class RideModel(Base):  # type: ignore
    __tablename__ = 'ride'
    __table_args__ = {'schema': 'cccat14'}

    ride_id = Column(UUID, primary_key=True)
    passenger_id = Column(String, nullable=True)
    driver_id = Column(String, nullable=True)
    status = Column(String, nullable=True)
    fare = Column(Numeric, nullable=True)
    distance = Column(Numeric, nullable=True)
    from_lat = Column(Numeric, nullable=True)
    from_long = Column(Numeric, nullable=True)
    to_lat = Column(Numeric, nullable=True)
    to_long = Column(Numeric, nullable=True)
    date = Column(DateTime, nullable=True)
