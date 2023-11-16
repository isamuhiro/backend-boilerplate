from typing import List, Optional

from domain.entities.ride import Ride, RideCreation
from domain.repositories.ride import RideRepository
from infra.database.connection import session
from infra.database.models.ride import RideModel


class DatabaseRideRepository(RideRepository):
    def find_by_passenger_id(self, id: str) -> Optional[Ride]:
        existing_ride_model = session.query(RideModel).filter_by(passenger_id=id).first()
        if not existing_ride_model:
            return None
        return Ride(**existing_ride_model)

    def create(self, ride_creation: RideCreation) -> Ride:
        ride_model = RideModel(**ride_creation.model_dump(), status="REQUESTED")
        session.add(ride_model)
        session.commit()
        
        return Ride(**ride_model)
