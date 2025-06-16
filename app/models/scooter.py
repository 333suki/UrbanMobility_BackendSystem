from datetime import datetime

class Scooter:
    def __init__(self, ID: int, serial_number: str, brand: str, model: str, top_speed: int, battery_capacity: int, state_of_charge: int, target_range_soc: str, location: str, out_of_service_status: int, mileage: int, last_maintenance_date: datetime):
        self.ID: int = ID
        self.serial_number: str = serial_number
        self.brand: str = brand
        self.model: str = model
        self.top_speed: int = top_speed
        self.battery_capacity: int = battery_capacity
        self.state_of_charge: int = state_of_charge
        self.target_rance_soc: tuple[int, int] = (int(target_range_soc.split(":")[0].strip()), int(target_range_soc.split(":")[1].strip()))
        self.location: str = location
        self.out_of_service_status: int = out_of_service_status
        self.mileage: int = mileage
        self.last_maintenance_date: datetime = last_maintenance_date
