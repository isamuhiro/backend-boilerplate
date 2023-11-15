import re
from typing import Optional


def is_plate_valid(plate: Optional[str]) -> bool:
    if not plate:
        return False
    plate = clean_plate(plate)
    plates = {
        'general': re.match(r'^[a-zA-Z]{3}[0-9]{4}$', plate),
        'car_mercosul': re.match(r'^[a-zA-Z]{3}[0-9]{1}[a-zA-Z]{1}[0-9]{2}$', plate),
        'motocycle_mercosul': re.match(r'^[a-zA-Z]{3}[0-9]{2}[a-zA-Z]{1}[0-9]{1}$', plate)
    }

    return any(result for result in list(plates.values()) if bool(result))


def clean_plate(plate: str) -> str:
    plate = re.sub(r'[^a-zA-Z0-9]', '', plate)
    return plate
