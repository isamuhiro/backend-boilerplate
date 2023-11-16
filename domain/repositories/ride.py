from typing import List, Optional
from abc import ABC, abstractmethod

from domain.entities.ride import Ride, RideCreation


class RepositoryRepository(ABC):
    @abstractmethod
    def find_ride_by_passenger_id(self, id: str) -> Optional[Ride]:
        pass

    @abstractmethod
    def create(self, ride_creation: RideCreation) -> Ride:
        pass
