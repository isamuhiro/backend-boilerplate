from datetime import datetime

from pydantic import BaseModel

from domain.entities.ride import RideCreation
from domain.exceptions.account import (AccountIsNotPassengerException,
                                       AccountNotFoundException)
from domain.exceptions.ride import InvalidRideStatusException
from domain.repositories.account import AccountRepository
from domain.repositories.ride import RideRepository


class Input(BaseModel):
    passenger_id: str
    from_lat: float
    from_long: float
    to_lat: float
    to_long: float
    date: datetime


class RequestRide():
    def __init__(self, account_repository: AccountRepository, ride_repository: RideRepository) -> None:
        self.account_repository = account_repository
        self.ride_repository = ride_repository

    def execute(self, input: Input) -> str:
        existing_passenger = self.account_repository.find_by_id(id=input.passenger_id)
        if not existing_passenger:
            raise AccountNotFoundException
        if not existing_passenger.is_passenger:
            raise AccountIsNotPassengerException

        ride = self.ride_repository.find_by_passenger_id(id=input.passenger_id)

        if not ride:
            ride = self.ride_repository.create(RideCreation(**input.model_dump()))

        if ride.status != "COMPLETED":
            raise InvalidRideStatusException

        return ride.ride_id
