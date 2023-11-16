from datetime import datetime
from typing_extensions import Unpack
from pydantic import BaseModel
from typing import Optional


class Ride(BaseModel):
    ride_id: str
    passenger_id: Optional[str]
    driver_id: Optional[str]
    status: Optional[str]
    fare: Optional[float]
    distance: Optional[float]
    from_lat: Optional[float]
    from_long: Optional[float]
    to_lat: Optional[float]
    to_long: Optional[float]
    date: Optional[datetime]


class RideCreation(BaseModel):
    passenger_id: str
    from_lat: float
    from_long: float
    to_lat: float
    to_long: float
